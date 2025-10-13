# --- Input Data ---
my_reg = "2023-CS-094"
timeline_string_to_check = "##__!_#!!__###"

# --- Derive Personalized Limits from REG ---
# A simple way to get some numbers from the registration number
m_max_hashtags = int(my_reg[-1]) # Max hashtag blocks is the last digit
n_cooldown_period = int(my_reg[0]) # Cooldown period is the first digit
k_max_consecutive_bangs = int(my_reg[-2]) # Max '!' is the second to last digit

# --- DFA State Initialization ---
# Using integers as flags, like a beginner might
is_in_hashtag_block = 0 # 0 for False, 1 for True
hashtag_blocks_count = 0
cooldown_counter = 0
bang_run_count = 0

# --- Rejection Flag ---
final_decision = "ACCEPT"

# --- Process the Timeline String ---
for character in timeline_string_to_check:

    if character == '#':
        # This is the start of a new hashtag block
        if is_in_hashtag_block == 0:
            # Check if cooldown period was met
            if hashtag_blocks_count > 0 and cooldown_counter < n_cooldown_period:
                final_decision = "REJECT"
                break
            
            # Check if we have exceeded the max number of blocks allowed
            if hashtag_blocks_count >= m_max_hashtags:
                final_decision = "REJECT"
                break
            
            # Update state for entering a new hashtag block
            is_in_hashtag_block = 1
            cooldown_counter = 0
        
        # We are continuing a hashtag block, so reset the bang counter
        bang_run_count = 0

    elif character == '_' or character == '!':
        # This is the end of a hashtag block
        if is_in_hashtag_block == 1:
            hashtag_blocks_count = hashtag_blocks_count + 1
            is_in_hashtag_block = 0
        
        # If we are not in a hashtag block, we are in a cooldown period
        if is_in_hashtag_block == 0:
            cooldown_counter = cooldown_counter + 1

        # Handle the logic for consecutive '!' characters
        if character == '!':
            bang_run_count = bang_run_count + 1
        else:
            bang_run_count = 0 # Reset if the character is '_'

        # Check if the '!' run exceeds the limit
        if bang_run_count > k_max_consecutive_bangs:
            final_decision = "REJECT"
            break
            
    else:
        # Invalid character found in the timeline
        final_decision = "REJECT"
        break

# --- Final Checks After the Loop ---
# If the loop finished while still inside a hashtag block, it counts as one more block
if is_in_hashtag_block == 1:
    hashtag_blocks_count = hashtag_blocks_count + 1

# Check if the total number of blocks exceeds the maximum allowed
if hashtag_blocks_count > m_max_hashtags:
    final_decision = "REJECT"

# --- Print the Final Result ---
print(final_decision)