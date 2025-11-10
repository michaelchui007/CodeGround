"""图书库管理系统CSV数据生成器"""
from pathlib import Path
import csv
import random
import datetime
import pathlib

import os
csv_path = os.path.join(os.path.dirname(__file__), 'data.csv')
OUT: Path = pathlib.Path(csv_path)

TITLE_ROW = 1
ROWS = 100000
random.seed(a=42)

total_length = ROWS + TITLE_ROW + 1
print(f'total length={total_length}')

# 图书库管理数据字段
# book_id: 图书编号
# isbn: 国际标准书号
# title: 书名
# author: 作者
# publisher: 出版社
# category: 分类
# publish_date: 出版日期
# price: 价格
# stock: 库存数量
# borrowed: 已借出数量
# status: 状态 (在架/借出/维修/下架)

# 预定义数据

categories = [
    '文学', '历史', '哲学', '艺术', '社会科学', '自然科学',
    '工业技术', '计算机', '经济', '管理', '教育', '语言',
    '小说', '诗歌', '散文', '传记'
]

authors = [
    '鲁迅', '老舍', '巴金', '茅盾', '钱钟书', '沈从文', '张爱玲', '冰心',
    '曹雪芹', '吴承恩', '施耐庵', '罗贯中', '金庸', '古龙', '梁羽生',
    '莫言', '余华', '王小波', '刘慈欣', '韩寒', '郭敬明', '安妮宝贝'
]

classic_titles = [
    '红楼梦', '三国演义', '水浒传', '西游记', '平凡的世界',
    '活着', '围城', '骆驼祥子', '朝花夕拾', '呐喊',
    '三体', '球状闪电', '流浪地球', '白鹿原', '废都'
]

publishers = [
    '人民文学出版社', '作家出版社', '中华书局', '商务印书馆', '三联书店',
    '上海译文出版社', '北京大学出版社', '清华大学出版社', '机械工业出版社',
    '电子工业出版社', '科学出版社', '高等教育出版社'
]

title_prefixes = [
    '论', '谈', '读', '看', '解读', '深入理解', '实战',
    '从零开始', '精通', '入门', '进阶', '高级', '权威指南'
]

title_subjects = [
    '人性', '社会', '历史', '文化', '艺术', '科学', '技术',
    '管理', '经济', '教育', '语言', '思维', '创新', '未来'
]

statuses = ['在架', '借出', '维修', '下架']
notes_options = ['', '热门', '新书', '推荐', '畅销', '经典', '珍藏版']

# 生成用户ID池
user_ids = [f'U{i:06d}' for i in range(1, 5001)]

with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    
    # 第一行：总行数
    w.writerow([total_length])
    
    # 第二行：表头（按分类、作者、书名的顺序）
    # w.writerow([
    #     'category', 'author', 'title', 'book_id', 'isbn',
    #     'publisher', 'publish_date', 'price', 'stock', 
    #     'borrowed', 'borrower_id', 'status', 'notes'
    # ])
    w.writerow([
        'category', 'author', 'title', 'book_id', 
        'publisher', 'publish_date', 
        'borrowed',  'notes','color'
    ])
    
    # 先生成所有数据到列表中
    all_data = []
    
    # 数据行
    for i in range(ROWS):
        book_id = f'BK{i+1:08d}'
        
        # 生成ISBN (简化版13位)
        isbn = f'978-7-{random.randint(100,999)}-{random.randint(10000,99999)}-{random.randint(0,9)}'
        
        # 生成书名
        if random.random() < 0.3:
            # 30%经典书名
            
            title = random.choice(classic_titles)
        else:
            # 70%组合书名
            title = f"{random.choice(title_prefixes)}{random.choice(title_subjects)}"
        
        author = random.choice(authors)
        publisher = random.choice(publishers)
        category = random.choice(categories)
        
        # 出版日期 (1990-2024)
        start_date = datetime.date(1990, 1, 1)
        end_date = datetime.date(2024, 12, 31)
        days_between = (end_date - start_date).days
        random_days = random.randint(0, days_between)
        publish_date = start_date + datetime.timedelta(days=random_days)
        publish_date_str = publish_date.strftime('%Y-%m-%d')
        
        # 价格 (10-500元)
        price = round(random.uniform(10.0, 500.0), 2)
        
        # 库存和借出
        stock = random.randint(1, 50)
        borrowed = random.randint(0, min(stock, 10))
        
        # 借阅者ID (如果有借出)
        borrower_id = random.choice(user_ids) if borrowed > 0 else ''
        
        # 状态 (借出比例更高)
        if borrowed > 0:
            status = '借出' if random.random() < 0.8 else random.choice(statuses)
        else:
            status = random.choice(['在架', '维修', '下架'])
        
        # 备注
        
        #notes = random.choice(notes_options)
        notes = notes_options[1]

        #颜色
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        
        # 添加到列表（按分类、作者、书名的顺序）
        # all_data.append([
        #     category, author, title, book_id, isbn,
        #     publisher, publish_date_str, price, stock,
        #     borrowed, borrower_id, status, notes
        # ])
        all_data.append([
            category, author, title, book_id, 
            publisher, publish_date_str, 
            borrowed,  notes,color
        ])
        
        # 进度提示
        if (i + 1) % 10000 == 0:
            print(f'已生成 {i + 1} / {ROWS} 行数据...')
    
    # 按照分类→作者→书名的顺序排序（树形结构）
    print('\n正在排序数据...')
    all_data.sort(key=lambda row: (row[0], row[1], row[2]))  # category, author, title
    print('排序完成！')
    
    # 写入排序后的数据
    print('正在写入文件...')
    for row in all_data:
        w.writerow(row)

print(f'\n数据生成完成！文件保存在: {OUT.absolute()}')
print(f'总行数: {total_length} (包含总行数行 + 表头行 + {ROWS}条数据)')
print('\n数据统计方案：')
print(f'1. 图书总数: {ROWS}本')
print(f'2. 作者数量: {len(authors)}位')
print(f'3. 出版社数量: {len(publishers)}家')
print(f'4. 图书分类: {len(categories)}个')
print(f'5. 用户数量: {len(user_ids)}人')
print('6. 时间跨度: 1990-2024年')
print('7. 价格区间: 10-500元')
print(f'8. 状态类型: {len(statuses)}种 (在架/借出/维修/下架)')