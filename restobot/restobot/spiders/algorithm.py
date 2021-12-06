import json


def getJson(expr):
    expr = expr.split('"sections":')
    if len(expr) < 2:
        # print("less than 2")
        return
    expr = expr[1]
    stack = []
    for ind, char in enumerate(expr):
        if char in ["(", "{", "["]:
            stack.append(char)
        elif char not in [")", "}", "]"]:
            pass
        else:
            if not stack:
                # print("stack is empty")
                return False
            # print(f" stack is {stack}")
            current_char = stack.pop()
            # print(f" we poped {current_char} from stack")
            if current_char == '(':
                if char != ")":
                    return False
            if current_char == '{':
                if char != "}":
                    return False
            if current_char == '[':
                if char != "]":
                    return False
            if not stack:
                # for i in range(10):
                #     print("*"*20)
                #     print()
                # print(f"end index {ind}")
                return json.loads(expr[0:ind+1])



def get_phone_list(test):
    num_list = []
    for item in test:
        build = False
        res = ""
        for ind, char in enumerate(item):
            if build:
                if char == "<":
                    num_list.append(res)
                    break
                res += char
                continue
            if char == "(":
                if item[ind + 4] == ")":
                    res += char
                    build = True
    return num_list




def get_image_list(myresult):
    img_list = []
    for test in myresult:
        build = False
        res = ""
        for char in test:
            if char == ")":
                img_list.append(res)
                break
            if build == True:
                res += char
            if char == "(":
                build = True
    return img_list


def get_ird(param):
    rid = 0
    for c in param.split():
        if "rid" in c:
            for i in c.split(","):
                if "rid" in i:
                    try:
                        rid = int(i[6:])
                    except:
                        continue
    return rid