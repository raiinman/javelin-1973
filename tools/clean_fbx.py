"""Remove export provenance and local paths without changing FBX asset data."""
import re
import struct
from pathlib import Path


def clean_fbx(path):
    path = Path(path)
    data = path.read_bytes()
    if not data.startswith(b'Kaydara FBX Binary  \x00\x1a\x00'):
        raise ValueError('Expected binary FBX')
    wide = struct.unpack_from('<I', data, 23)[0] >= 7500
    header = struct.Struct('<QQQB' if wide else '<IIIB')
    null = bytes(header.size)
    provenance = {b'Creator', b'CreationTime', b'CreationTimeStamp', b'SceneInfo', b'FileId'}

    def properties(raw, count, filename):
        result = bytearray()
        pos = 0
        for _ in range(count):
            start = pos
            kind = raw[pos:pos+1]
            pos += 1
            if kind in (b'S', b'R'):
                size = struct.unpack_from('<I', raw, pos)[0]
                value = raw[pos+4:pos+4+size]
                pos += 4+size
                if kind == b'S' and (filename or re.match(rb'^(?:[A-Za-z]:[/\\]|\\\\|/)', value)):
                    value = re.split(rb'[/\\]', value)[-1]
                    result.extend(kind + struct.pack('<I', len(value)) + value)
                    continue
            elif kind in (b'f', b'd', b'l', b'i', b'b', b'c'):
                size = struct.unpack_from('<III', raw, pos)[2]
                pos += 12+size
            else:
                widths = {b'Y': 2, b'C': 1, b'I': 4, b'F': 4, b'D': 8, b'L': 8}
                if kind not in widths:
                    raise ValueError(f'Unsupported FBX property {kind!r}')
                pos += widths[kind]
            result.extend(raw[start:pos])
        if pos != len(raw):
            raise ValueError('Invalid FBX property length')
        return bytes(result)

    def node(pos, output_pos):
        end, count, length, name_length = header.unpack_from(data, pos)
        name_start = pos+header.size
        name = data[name_start:name_start+name_length]
        if end <= pos or end > len(data):
            raise ValueError('Invalid FBX node bounds')
        if name in provenance:
            return end, b''
        prop_start = name_start+name_length
        props = properties(data[prop_start:prop_start+length], count,
                           name in (b'FileName', b'Filename', b'RelativeFilename'))
        prefix_size = header.size+len(name)+len(props)
        children = bytearray()
        child_pos = prop_start+length
        while child_pos < end:
            if data[child_pos:child_pos+header.size] == null:
                children.extend(null)
                child_pos += header.size
                break
            child_pos, child = node(child_pos, output_pos+prefix_size+len(children))
            children.extend(child)
        if child_pos != end:
            raise ValueError('Invalid FBX child bounds')
        output_end = output_pos+prefix_size+len(children)
        return end, header.pack(output_end, count, len(props), len(name))+name+props+children

    output = bytearray(data[:27])
    pos = 27
    while data[pos:pos+header.size] != null:
        pos, chunk = node(pos, len(output))
        output.extend(chunk)
    output.extend(data[pos:])
    path.write_bytes(output)


if __name__ == '__main__':
    import sys
    for argument in sys.argv[1:]:
        clean_fbx(argument)
