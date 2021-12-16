import sys
import classes
Item = classes.Item
from classes import Item

sys.stdout.write("this is a to-do list\n")

# words = {"hello": "a greeting",
#    "world": "the planet"
# }
# print(words["hello"])


items = []


def addCommand():
    print("Enter new item:")
    item = input()
    items.append(Item(item))


def removeCommand():
    print("Enter number of item to remove:")
    index = int(input())
    # items[index-1:index] = []
    del items[index - 1]


def markDone():
    print("Enter number of item to remove:")
    index = int(input())
    items[index - 1].finish()


def justCompletedItems():
    return [it.text for it in items if it.complete]


# [ x * x for x in range(10) ]

def showComplete():
    for it in justCompletedItems():
        print(it)


def justUncompletedItems():
    for it in items:
        if not it.complete:
            yield it.text


def showIncomplete():
    for it in justUncompletedItems():
        print(it)


def save():
    with open("todo.txt", "w") as fp:
        for it in items:
            fp.write("complete " if it.complete else "incomplete ")
            fp.write(it.text)
            fp.write("\n")


try:
    with open("todo.txt", "r") as fp:
        for line in fp.readlines():
            complete, text = line.split(' ', 1)
            items.append(Item(text.strip(), complete == 'complete'))
except IOError:
    pass
finally:
    pass

while True:
    index = 1
    for it in items:
        print(str(index) + ". " + str(it))
        if isinstance(it, str):
            print("it's a string")
        index += 1
    print("Enter command: add remove done show-complete show-incomplete")
    command = input()
    if command == "add":
        addCommand()
    elif command == "remove":
        removeCommand()
    elif command == "done":
        markDone()
    elif command == "show-complete":
        showComplete()
    elif command == "show-incomplete":
        showIncomplete()
    save()
