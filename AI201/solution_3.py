my_reg = "2023-CS-094"
timeline_string_to_check = "##__!_#!!__###"


m_max_hashtags = int(my_reg[-1]) 
n_cooldown_period = int(my_reg[0]) 
k_max_consecutive_bangs = int(my_reg[-2]) 

is_in_hashtag_block = 0 
hashtag_blocks_count = 0
cooldown_counter = 0
bang_run_count = 0

final_decision = "ACCEPT"

for character in timeline_string_to_check:

    if character == '#':

        if is_in_hashtag_block == 0:

            if hashtag_blocks_count > 0 and cooldown_counter < n_cooldown_period:
                final_decision = "REJECT"
                break
            
            if hashtag_blocks_count >= m_max_hashtags:
                final_decision = "REJECT"
                break
            
            is_in_hashtag_block = 1
            cooldown_counter = 0
        
        bang_run_count = 0

    elif character == '_' or character == '!':

        if is_in_hashtag_block == 1:
            hashtag_blocks_count = hashtag_blocks_count + 1
            is_in_hashtag_block = 0
        
        if is_in_hashtag_block == 0:
            cooldown_counter = cooldown_counter + 1

        if character == '!':
            bang_run_count = bang_run_count + 1
        else:
            bang_run_count = 0

        if bang_run_count > k_max_consecutive_bangs:
            final_decision = "REJECT"
            break
            
    else:
        final_decision = "REJECT"
        break

if is_in_hashtag_block == 1:
    hashtag_blocks_count = hashtag_blocks_count + 1

if hashtag_blocks_count > m_max_hashtags:
    final_decision = "REJECT"

print(final_decision)