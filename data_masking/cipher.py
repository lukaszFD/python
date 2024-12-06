import hashlib

# Transformation for ID
ID_MAPPING = {'1': '9', '2': '8', '3': '4', '4': '7', '5': '6',
              '6': '0', '7': '3', '8': '1', '9': '5', '0': '2'}

def transform_id(id_value):
    """Transforms an ID based on predefined mapping."""
    return ''.join(ID_MAPPING.get(char, char) for char in id_value)

# Transformation for Host
HOST_MAPPING = {'x': 'b', 'y': 'f', 'u': 'b', 'z': 'g', 'v': 'h'}

def transform_host(host_value):
    """Transforms host string based on predefined mapping."""
    return ''.join(HOST_MAPPING.get(char, char) for char in host_value)

# Hashing for Name
def hash_name(name_value):
    """Hashes name using SHA-256."""
    return hashlib.sha256(name_value.encode()).hexdigest()

def reverse_transform_id(masked_id):
    """Reverses the ID transformation."""
    transform_map = {'9': '1', '8': '2', '4': '3', '7': '4', '6': '5',
                     '0': '6', '3': '7', '1': '8', '5': '9', '2': '0'}
    return ''.join(transform_map[char] for char in masked_id)

def reverse_transform_host(masked_host):
    """Reverses the host transformation."""
    transform_map = {'b': 'x', 'f': 'y', 'b': 'u', 'g': 'z', 'h': 'v', 'k': 'v'}
    return ''.join(transform_map.get(char, char) for char in masked_host)
