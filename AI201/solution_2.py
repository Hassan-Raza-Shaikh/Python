student_name = "Ayesha Asif Siddiqui"
student_reg = "2022-CS-058"

name_parts_list = student_name.split(' ')

first_token = name_parts_list[0]
last_token = name_parts_list[-1]
middle_tokens_list = name_parts_list[1:-1]
middle_tokens_as_tuple = tuple(middle_tokens_list)

reg_digits_part1 = student_reg[0:4]
reg_digits_part2 = student_reg[8:11]
all_reg_digits = reg_digits_part1 + reg_digits_part2

even_digits = all_reg_digits[0::2]
odd_digits = all_reg_digits[1::2]

initial_data = [first_token, middle_tokens_as_tuple, last_token, [even_digits, odd_digits]]

handle_string = "@" + first_token + last_token

tag_string = even_digits[::-1]

name_without_spaces = student_name.replace(" ", "")
name_len_val = len(name_without_spaces)
length_marker_str = str(name_len_val)

initial_data[-1:] = [("MUTATED", tag_string)]

output_handle_part = "| @" + handle_string + " |"
output_tag_part = " tag:" + tag_string + " |"
output_len_part = " len:" + length_marker_str + " |"
output_data_part = " data:" + str(initial_data)

final_prompt_card = output_handle_part + output_tag_part + output_len_part + output_data_part

print(final_prompt_card)