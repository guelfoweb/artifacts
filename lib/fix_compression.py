import os
import struct
from typing import Optional, List

# ref. https://www.iana.org/assignments/media-types/application/zip
# check APK with exiftool

class DataView:
    """Helper class for reading and writing binary data with offset tracking."""
    
    def __init__(self, data: bytes):
        self.data = bytearray(data)
        self.offset = 0

    def read(self, n: int) -> bytes:
        """Read n bytes from current offset."""
        result = self.data[self.offset:self.offset + n]
        self.offset += n
        return result
    
    def set_offset(self, offset: int) -> 'DataView':
        """Set absolute offset position."""
        self.offset = offset
        return self
    
    def skip(self, n: int) -> 'DataView':
        """Skip n bytes forward."""
        self.offset += n 
        return self

    @staticmethod
    def _format_size(format: str) -> int:
        """Calculate size needed for struct format."""
        to_size = {"H": 2, "I": 4, "B": 1, "<": 0}
        return sum(map(lambda c: to_size[c], format))
    
    def unpack(self, format: str) -> tuple:
        """Unpack data using struct format."""
        return struct.unpack(format, self.read(DataView._format_size(format)))

    def pack(self, format: str, *args) -> 'DataView':
        """Pack data at current offset."""
        patch = struct.pack(format, *args)
        size = len(patch)
        self.data[self.offset:self.offset + size] = patch 
        return self
    
    def move(self, offset: int, length: int) -> 'DataView':
        """Move a block of data by offset bytes."""
        block = self.data[self.offset : self.offset + length]
        self.data[self.offset + offset: self.offset + offset + length] = block 
        return self

class HeaderInfo:
    """ZIP header information structure."""
    
    def __init__(self, flag: int, compression: int, modified_time: int, 
                 modified_date: int, crc32: int, compressed_size: int, 
                 uncompressed_size: int, filename_len: int, extra_field_len: int):
        self.flag = flag
        self.compression = compression
        self.modified_time = modified_time
        self.modified_date = modified_date
        self.crc32 = crc32
        self.compressed_size = compressed_size
        self.uncompressed_size = uncompressed_size
        self.filename_len = filename_len
        self.extra_field_len = extra_field_len

    @staticmethod
    def parse(data: DataView) -> 'HeaderInfo':
        """Parse header info from data view."""
        flag, compression, modified_time, modified_date, crc32, \
            compressed_size, uncompressed_size, filename_len, extra_field_len \
            = data.unpack("<HHHHIIIHH")
        return HeaderInfo(flag, compression, modified_time, modified_date, crc32,
                          compressed_size, uncompressed_size, filename_len, extra_field_len)

class LocalHeader:
    """ZIP Local File Header structure."""
    
    def __init__(self, offset: int, signature: int, version: int, 
                 info: HeaderInfo, filename: bytes, extra: bytes):
        self.offset = offset
        self.signature = signature
        self.version = version
        self.info = info
        self.filename = filename
        self.extra = extra

    @staticmethod
    def parse(data: DataView) -> 'LocalHeader':  
        """Parse local header from data view."""
        offset = data.offset
        signature, version = data.unpack("<IH")
        if signature != 0x04034b50:
            raise ValueError(f"Invalid Local Header at offset {hex(offset)}")
        info = HeaderInfo.parse(data)
        filename = data.read(info.filename_len)
        extra = data.read(info.extra_field_len)
        return LocalHeader(offset, signature, version, info, filename, extra)

class CentralDirectoryHeader:
    """ZIP Central Directory Header structure."""
    
    def __init__(self, offset: int, signature: int, version: int, version_needed: int,
                 info: HeaderInfo, comment_len: int, disk_start: int, internal_attr: int,
                 external_attr: int, localheader_offset: int, filename: bytes, 
                 extra: bytes, comment: bytes):
        self.offset = offset
        self.signature = signature
        self.version = version
        self.version_needed = version_needed
        self.info = info
        self.comment_len = comment_len
        self.disk_start = disk_start
        self.internal_attr = internal_attr
        self.external_attr = external_attr
        self.localheader_offset = localheader_offset
        self.filename = filename
        self.extra = extra
        self.comment = comment

    @staticmethod
    def parse(data: DataView) -> 'CentralDirectoryHeader':
        """Parse central directory header from data view."""
        offset = data.offset
        signature, version, version_needed = data.unpack("<IHH")
        if signature != 0x02014b50:
            raise ValueError(f"Invalid Central Directory Header at offset {hex(offset)}")
        info = HeaderInfo.parse(data)
        comment_len, disk_start, internal_attr, external_attr, localheader_offset \
            = data.unpack("<HHHII")
        filename = data.read(info.filename_len)
        extra = data.read(info.extra_field_len)
        comment = data.read(comment_len)
        return CentralDirectoryHeader(offset, signature, version, version_needed, info, comment_len, 
                                      disk_start, internal_attr, external_attr, localheader_offset,
                                      filename, extra, comment)

class ZipHeaderFixer:
    """
    A class to fix corrupted ZIP file headers by fixing compression issues
    and synchronizing Central Directory and Local File Header inconsistencies.
    """
    
    def __init__(self, zip_path: str, verbose: bool = False):
        """
        Initialize the ZipHeaderFixer with a ZIP file path.
        
        Args:
            zip_path: Path to the ZIP file to be fixed
            verbose: Enable verbose output
        """
        self.zip_path = zip_path
        self.verbose = verbose
        self.corruption_issues = []
        
    def _log(self, message: str):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[LOG] {message}")
            
    def _print(self, message: str):
        """Always print message."""
        print(message)
        
    def check_and_fix(self) -> str:
        """
        Check if ZIP file is corrupted and ask user if they want to fix it.
        If user agrees, creates a fixed version with '_fixed' suffix.
        
        Returns:
            'healthy' - File is already correct, no issues found
            'fixed' - File had issues and was successfully fixed
            'cancelled' - File has issues but user chose not to fix
            'error' - An error occurred during the process
        """
        if not os.path.exists(self.zip_path):
            print(f"Error: File {self.zip_path} not found")
            return 'error'
            
        # Check for corruption
        try:
            issues = self._check_corruption()
            if not issues:
                print("ZIP file appears to be healthy - no issues detected")
                return 'healthy'
                
            # Report issues found
            print(f"\nZIP file corruption detected! Found {len(issues)} issues:")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
                
            # Ask user if they want to proceed with fix
            while True:
                response = input("\nDo you want to proceed with the fix? (y/n): ").lower().strip()
                if response in ['y', 'yes']:
                    break
                elif response in ['n', 'no']:
                    print("Fix cancelled by user")
                    return 'cancelled'
                else:
                    print("Please enter 'y' for yes or 'n' for no")
                    
            # Create output filename with '_fixed' suffix
            base, ext = os.path.splitext(self.zip_path)
            output_path = f"{base}_fixed{ext}"
            
            if self._fix_zip_file(output_path):
                return 'fixed'
            else:
                return 'error'
                
        except Exception as e:
            print(f"Error during check: {e}")
            return 'error'
    
    def _check_corruption(self) -> List[str]:
        """
        Check ZIP file for corruption issues.
        
        Returns:
            List of issues found
        """
        issues = []
        
        try:
            with open(self.zip_path, 'rb') as f:
                data = f.read()
                
            # Find End of Central Directory Record
            try:
                eocd_offset = data.rindex(b"PK\x05\x06")
            except ValueError:
                issues.append("End of Central Directory record not found")
                return issues
                
            self._log(f"Found EOCD at offset {hex(eocd_offset)}")
            
            data_view = DataView(data)
            data_view.set_offset(eocd_offset + 0xa)
            cd_n_entries, _, cd_offset = data_view.unpack("<HII")
            
            self._log(f"Central Directory at {hex(cd_offset)} with {cd_n_entries} entries")
            
            # Parse Central Directory entries
            data_view.set_offset(cd_offset)
            cd_entries = []
            
            for i in range(cd_n_entries):
                try:
                    cd_entry = CentralDirectoryHeader.parse(data_view)
                    cd_entries.append(cd_entry)
                    
                    # Check for unsupported compression
                    if cd_entry.info.compression not in [0, 8]:
                        filename = cd_entry.filename.decode('utf-8', errors='ignore')
                        issues.append(f"Unsupported compression method {cd_entry.info.compression} in '{filename}'")
                        
                except Exception as e:
                    issues.append(f"Corrupted Central Directory entry {i}: {e}")
                    continue
            
            # Check Local Headers
            for i, cd_entry in enumerate(cd_entries):
                try:
                    data_view.set_offset(cd_entry.localheader_offset)
                    local_header = LocalHeader.parse(data_view)
                    
                    # Check for compression mismatch
                    if local_header.info.compression != cd_entry.info.compression:
                        filename = cd_entry.filename.decode('utf-8', errors='ignore')
                        issues.append(f"Compression mismatch in '{filename}': CD={cd_entry.info.compression}, Local={local_header.info.compression}")
                        
                    # Check for unsupported compression in local header
                    if local_header.info.compression not in [0, 8]:
                        filename = local_header.filename.decode('utf-8', errors='ignore')
                        issues.append(f"Unsupported compression method {local_header.info.compression} in local header for '{filename}'")
                        
                except Exception as e:
                    issues.append(f"Corrupted Local Header for entry {i}: {e}")
                    
        except Exception as e:
            issues.append(f"Severe corruption: {e}")
            
        return issues
    
    def _fix_zip_file(self, output_path: str) -> bool:
        """
        Fix the ZIP file and save to output path.
        
        Args:
            output_path: Path for the fixed file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.zip_path, 'rb') as f:
                file_data = f.read()
                
            # Find EOCD
            eocd_offset = file_data.rindex(b"PK\x05\x06")
            #self._log(f"Found End of Central Directory record at offset {hex(eocd_offset)}")

            data = DataView(file_data)
            data.set_offset(eocd_offset + 0xa)
            cd_n_entries, _, cd_offset = data.unpack("<HII")

            self._log(f"Central Directory starts at {hex(cd_offset)} and has {cd_n_entries} entries")

            # Parse Central Directory entries
            data.set_offset(cd_offset)
            cd_entries = []
            for _ in range(cd_n_entries):
                cd_entries.append(CentralDirectoryHeader.parse(data))
                
            # Parse Local Headers
            loc_headers = []
            for cd in cd_entries:
                data.set_offset(cd.localheader_offset)
                loc_headers.append(LocalHeader.parse(data))

            fixes_applied = 0
            
            
            # Fix Central Directory entries
            for cd in cd_entries:
                if cd.info.compression not in [0, 8]:
                    filename = cd.filename.decode("utf-8", errors='ignore')
                    self._print(f"Fixing Central Directory header for '{filename}' at offset {hex(cd.offset)}")
                    
                    # Fix compression type, set to none (0)
                    data.set_offset(cd.offset + 0x0a).pack("<H", 0)
                    # Fix compressed size to match uncompressed size
                    data.set_offset(cd.offset + 0x14).pack("<I", cd.info.uncompressed_size)
                    fixes_applied += 1
            
            # Fix Local Headers
            for local_header in loc_headers:
                if local_header.info.compression not in [0, 8]:
                    filename = local_header.filename.decode("utf-8", errors='ignore')
                    self._print(f"Fixing Local header for '{filename}' at offset {hex(local_header.offset)}")
                    
                    # Fix compression type, set to none (0)
                    data.set_offset(local_header.offset + 0x08).pack("<H", 0)
                    # Fix compressed size
                    data.set_offset(local_header.offset + 0x12).pack("<I", local_header.info.uncompressed_size)

                    # Remove extra bytes if present
                    if local_header.info.extra_field_len > 0:
                        data.set_offset(local_header.offset + 0x1c).pack("<H", 0)
                        data.set_offset(local_header.offset + 0x1e + local_header.info.filename_len + local_header.info.extra_field_len).move(-local_header.info.extra_field_len, local_header.info.uncompressed_size)
                    
                    fixes_applied += 1

            # Save fixed file
            with open(output_path, "wb") as f:
                f.write(data.data)
                
            self._print(f"Successfully applied {fixes_applied} fixes to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error fixing ZIP file: {e}")
            return False
