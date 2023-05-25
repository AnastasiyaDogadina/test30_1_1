from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.implicitly_wait(10)

driver.get("https://petfriends.skillfactory.ru/my_pets")


def get_count_pets():
    panel = driver.find_elements(By.CSS_SELECTOR, "body div.fill.task2 div.fill.task3 div.left")
    return int(panel[0].text.split("Питомцев: ")[-1].split('\n')[0])


def get_pet_blocks():
    return driver.find_element(By.ID, "all_my_pets").find_elements(By.TAG_NAME, "tbody")[0]


def is_pet_stack_full(ideal_count, blocks):
    return len(blocks.find_elements(By.TAG_NAME, "tr")) == ideal_count


def count_of_images(blocks):
    lisf_of_images = filter(lambda src: src != '',
                            [i.get_attribute('src') for i in blocks.find_elements(By.TAG_NAME, "img")])
    return len(list(lisf_of_images))


def get_pets_profiles(blocks):
    return [
        {"name": i.find_elements(By.TAG_NAME, "td")[0].text,
         "kind": i.find_elements(By.TAG_NAME, "td")[1].text,
         "age": i.find_elements(By.TAG_NAME, "td")[2].text} for i in blocks.find_elements(By.TAG_NAME, "tr")
    ]


def pets_profiles_is_full(profiles):
    for pet in profiles:
        for item in pet:
            if pet[item] == "":
                return False
    return True


def names_is_unique(profiles):
    names = [i["name"] for i in profiles]
    return len(list(set(names))) == len(names)


def profile_is_unique(profiles):
    seen_set = set()
    hash_wd = []
    for d in profiles:
        t = tuple(d.items())
        if t not in seen_set:
            seen_set.add(t)
            hash_wd.append(d)
    return len(profiles) == len(hash_wd)


pet_count = get_count_pets()
pet_blocks = get_pet_blocks()
current_count = is_pet_stack_full(pet_count, blocks=pet_blocks)

print("Real count of Pets:", pet_count)
print("Current count of pets:", current_count)
img_count = count_of_images(pet_blocks)
print("Count of images:", img_count, ", images more then half count of pets:", img_count >= pet_count / 2)
profiles = get_pets_profiles(pet_blocks)
print("Profiles is full:", pets_profiles_is_full(profiles))
print("Names is unique:", names_is_unique(profiles))
print("Profiles is unique:", profile_is_unique(profiles))
