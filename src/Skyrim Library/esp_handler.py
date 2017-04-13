
def get_esp_list(plugins_path):
    esp_list = []
    with open(plugins_path, 'r') as plugins_file:
        for i, line in enumerate(plugins_file):
            if line[0] == '#':
                continue
            esp_list.append(line)

    print("\n------------------------\n" + "ESP_list: " + esp_list + "\n------------------------\n")
    return esp_list
