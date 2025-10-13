my_name = "Zia Ahmed"
my_reg = "2023-CS-101"

emoji_set = ('🤖', '⚡', '🧠', '🎯', '🔥', '💀', '👽', '👾', '🚀', '⭐', '🌙', '☀️', '🌍', '🌊', '🌲', '💎')

# --- Derive Integers ---
name_without_spaces = my_name.replace(" ", "")
name_length_val = len(name_without_spaces)

reg_year_str = my_reg[0:4]
reg_roll_str = my_reg[8:11]

reg_year_int = int(reg_year_str)
reg_roll_int = int(reg_roll_str)

# --- Combine into 64-bit value ---
# Packing: [ 16 bits for year | 16 bits for roll number | 16 bits for name length | 16 bits for a constant ]
val1 = reg_year_int
val2 = reg_roll_int
val3 = name_length_val
val4 = 42

shifted_val1 = val1 << 48
shifted_val2 = val2 << 32
shifted_val3 = val3 << 16
shifted_val4 = val4

vibe_hash = shifted_val1 | shifted_val2 | shifted_val3 | shifted_val4

# --- Map nibbles to emojis ---
# Extracting a 16-bit chunk (4 nibbles) from the middle of the hash
sixteen_bit_chunk = (vibe_hash >> 24) & 0xFFFF

# Getting the index for each of the four emojis from the 16-bit chunk
index1 = (sixteen_bit_chunk >> 12) & 0xF
index2 = (sixteen_bit_chunk >> 8) & 0xF
index3 = (sixteen_bit_chunk >> 4) & 0xF
index4 = sixteen_bit_chunk & 0xF

emoji1 = emoji_set[index1]
emoji2 = emoji_set[index2]
emoji3 = emoji_set[index3]
emoji4 = emoji_set[index4]

# --- Print the final output ---
hex_value_str = hex(vibe_hash)
persona_str = ":" + emoji1 + "::" + emoji2 + "::" + emoji3 + "::" + emoji4

final_output = "hex=" + hex_value_str + " persona=" + persona_str

print(final_output)