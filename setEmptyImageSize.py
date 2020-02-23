import pickle
import json
import requests
from tqdm import  tqdm

data = {'PP1': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PP1&img=1&zoom=3&hl=en&sig=ACfU3U0QB2GP7uc99P7zcq7C0jNYsfaERQ', 'order': 0},
        'PT3': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT3&img=1&zoom=3&hl=en&sig=ACfU3U3joc6hGZD5iSjgfbnrd6K_GfW1zw', 'order': 3},
        'PT4': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT4&img=1&zoom=3&hl=en&sig=ACfU3U3DOQsXflQ68_BgcoQ_yr-TIRFC-w', 'order': 4},
        'PT5': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT5&img=1&zoom=3&hl=en&sig=ACfU3U3KexcOeKGHBgYsN79twL0m-2qVUw', 'order': 5},
        'PT6': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT6&img=1&zoom=3&hl=en&sig=ACfU3U2_KX6iW7VZq2OVNtvMwsqaZFR8NQ', 'order': 6},
        'PT7': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT7&img=1&zoom=3&hl=en&sig=ACfU3U24aglXX8G0uNUgjeeqNJ-TS44SfA', 'order': 7},
        'PT8': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT8&img=1&zoom=3&hl=en&sig=ACfU3U160CMcgO5mXYNwzLpn9WHSr2AdKw', 'order': 8},
        'PT9': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT9&img=1&zoom=3&hl=en&sig=ACfU3U23-zSSUmus3ai5I3A3KqstrXyfew', 'order': 9},
        'PT10': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT10&img=1&zoom=3&hl=en&sig=ACfU3U2CCzmHFcYfB3iOdJ4S3v3_GttnPQ', 'order': 10},
        'PT11': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT11&img=1&zoom=3&hl=en&sig=ACfU3U2oYmRoLU_cytQaqT20S1qWiQPavQ', 'order': 11},
        'PT12': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT12&img=1&zoom=3&hl=en&sig=ACfU3U0u2qeeBponQyiMRe-3DVQCj3GzZw', 'order': 12},
        'PT13': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT13&img=1&zoom=3&hl=en&sig=ACfU3U2asTfYXBg1TMRu4qYq24PjCOgM9A', 'order': 13},
        'PT14': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT14&img=1&zoom=3&hl=en&sig=ACfU3U1AXhkE_b5hN7CBVG3BHLC3O4TWaw', 'order': 14},
        'PT15': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT15&img=1&zoom=3&hl=en&sig=ACfU3U1vKrVz5yuFpLq3ICY1VRxEMrcMtw', 'order': 15},
        'PT16': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT16&img=1&zoom=3&hl=en&sig=ACfU3U1CYesXUc2SHKVR9ObplaiNJzXG5A', 'order': 16},
        'PT17': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT17&img=1&zoom=3&hl=en&sig=ACfU3U3iY6sPLliqKke214KcNKv_PiIYHg', 'order': 17},
        'PT18': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT18&img=1&zoom=3&hl=en&sig=ACfU3U29zeackoVKyATpEGmwPFeGQRuljw', 'order': 18},
        'PT19': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT19&img=1&zoom=3&hl=en&sig=ACfU3U06OVo4_8kVZvA_vhkR1Tir1-odOg', 'order': 19},
        'PT22': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT22&img=1&zoom=3&hl=en&sig=ACfU3U31XosYZh1i6LEzQVAvy2fRfQXg8Q', 'order': 22},
        'PT23': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT23&img=1&zoom=3&hl=en&sig=ACfU3U3y3QjR9jQrWaAv5nYT71k3Dhr3aA', 'order': 23},
        'PT24': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT24&img=1&zoom=3&hl=en&sig=ACfU3U3gaLoPz7vKiz80x-YYLj_q0HK0sw', 'order': 24},
        'PT25': {'src': 'https://books.google.co.in/books/content?id=LyIiDAAAQBAJ&pg=PT25&img=1&zoom=3&hl=en&sig=ACfU3U1xxMBiGYvvHzT3_stJLyBG0B0gZA', 'order': 25}}

with open('settings.json') as settingsFile:
    settings = json.load(settingsFile)

pageSizes = []
for page in tqdm(data.keys()):
    link = data[page]['src']+'&w=' + str(settings['page_resolution'])
    response = requests.get(link)
    pageSizes.append(len(response.content))

frequencyDict = {}

for a1 in pageSizes:
    try:
        frequencyDict[a1] +=1
    except:
        frequencyDict[a1] = 1

frequencyList = [[x,frequencyDict[x]] for x in frequencyDict.keys()]
frequencyList.sort(key=lambda x:x[1])
resolutionSize = frequencyList[-1][0]

print(f'------------------- Empty image size for current resolution changed to : {resolutionSize} -------------------')

settings['empty_image_size'] = resolutionSize
with open('settings.json','w') as settingsFile:
    json.dump(settings,settingsFile,indent=4)

