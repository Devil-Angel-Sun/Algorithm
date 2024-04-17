


def prettyXml(element, indent, newline, level = 0): 
    """
    对标签执行美化，为标签添加缩进
    Args:
        element:craet_xml中的Elment类
        indent:用于缩进
        newline:用于换行
        level:

    """
    # 判断element是否有子元素
    if element:  
        if element.text == None or element.text.isspace(): # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)

    # 将elemnt转成list
    temp = list(element) 
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作