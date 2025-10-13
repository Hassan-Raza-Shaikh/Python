# --- Personalization based on Name and Registration ---
my_name = "Junaid Saleem"
my_reg = "2023-CS-155"

# --- Class Definitions ---

class AgentBase:
    __boot_count = 0

    def __init__(self, initial_secret):
        self.__secret_code = initial_secret
        self.min_secret_length = len(my_name.split())
        AgentBase.__boot_count = AgentBase.__boot_count + 1

    def get_secret_code(self):
        return self.__secret_code

    def set_secret_code(self, new_secret_code):
        is_long_enough = len(new_secret_code) >= self.min_secret_length
        is_alphanumeric = new_secret_code.isalnum()

        if is_long_enough and is_alphanumeric:
            self.__secret_code = new_secret_code
            return True
        else:
            return False

class TokenMeter:
    def __init__(self, agent_id):
        self.agent_id_num = agent_id
        self.bias = 10

    def get_bias(self):
        return self.bias

    def set_bias(self, new_bias_value):
        self.bias = new_bias_value

    def get_token_reading(self):
        reading = (self.agent_id_num * 5) + self.bias
        return reading

class SimpleLogger:
    def __init__(self):
        self.log_records = []

    def log(self, entry):
        self.log_records.append(entry)

    def get_log_size(self):
        return len(self.log_records)

class NanoAgent(AgentBase, TokenMeter, SimpleLogger):
    __boot_count = 9999

    def __init__(self, agent_id, initial_secret):
        AgentBase.__init__(self, initial_secret)
        TokenMeter.__init__(self, agent_id)
        SimpleLogger.__init__(self)

    def perform_read_and_log(self):
        current_reading = self.get_token_reading()
        log_entry_to_add = (self.agent_id_num, current_reading)
        self.log(log_entry_to_add)


# --- Top-Level Demo ---

print("--- Starting Demo ---")

agent_id_from_reg = int(my_reg[-3:])
my_agent = NanoAgent(agent_id_from_reg, "initial123")

print("\n1. Boot Count and Attribute Shadowing:")
print("Base class boot count: " + str(AgentBase._AgentBase__boot_count))
print("NanoAgent class shadowed attribute: " + str(my_agent._NanoAgent__boot_count))

print("\n2. Encapsulation and Name Mangling:")
try:
    print(my_agent.__secret_code)
except AttributeError as e:
    print("Direct access failed as expected: " + str(e))

print("Access via name mangling: " + str(my_agent._AgentBase__secret_code))

print("\n3. Secret Update Validation:")
update_status_fail = my_agent.set_secret_code("!@#")
print("Attempting to set invalid secret '!@#': " + str(update_status_fail))
print("Current secret: " + my_agent.get_secret_code())

update_status_pass = my_agent.set_secret_code("newsecret456")
print("Attempting to set valid secret 'newsecret456': " + str(update_status_pass))
print("Current secret: " + my_agent.get_secret_code())

print("\n4. Meter Reading and Logging:")
print("Initial log size: " + str(my_agent.get_log_size()))

my_agent.perform_read_and_log()
print("Log size after first reading: " + str(my_agent.get_log_size()))

my_agent.set_bias(500)
print("Bias updated to 500")

my_agent.perform_read_and_log()
print("Log size after second reading: " + str(my_agent.get_log_size()))
print("Current log entries: " + str(my_agent.log_records))

print("\n--- Demo Finished ---")