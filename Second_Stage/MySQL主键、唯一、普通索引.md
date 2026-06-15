# MySQL 主键、唯一、普通索引

## 1.索引是什么？为什么需要索引？

索引是一种帮助数据库快速定位数据的数据结构，类似于书的目录。

索引虽然能加速查询，但是会降低写入速度，因为需要同时维护索引结构，且占用额外磁盘空间

## 2.三种索引的区别

| 索引类型                   | 约束             | 允许空值(NULL)         | 一个表可以有多个？                | 索引结构                    | 备注          |
| ---------------------- | -------------- | ------------------ | ------------------------ | ----------------------- | ----------- |
| **主键索引 (PRIMARY KEY)** | 唯一且非空          | 不允许NULL            | **只能有一个**，但可以是联合主键（多列组合） | InnoDB中为**聚簇索引**（数据即索引） | 主键是表的“行标识符” |
| **唯一索引 (UNIQUE)**      | 唯一（可以有多个NULL值） | 允许NULL（但NULL可以有多个） | 可以有多个                    | 辅助索引（二级索引）（非聚簇）         | 保证列值或组合值唯一  |
| **普通索引 (INDEX/KEY)**   | 无唯一约束          | 允许NULL             | 可以有多个                    | 辅助索引（二级索引）              | 仅加速查询，无约束功能 |

聚簇索引：InnoDB中，主键索引就是聚簇索引，子叶节点之间存储整行数据。所以通过主键查询最快

辅助索引：唯一索引和普通索引都是辅助索引，它们的子叶节点从存储的是主键值，而不是数据本身

# 3.如何定义索引和使用

### 3.1.主键索引

每个表只能有一个主键索引，值必须唯一且不为NULL

```sql
-- 单列主键
CREATE TABLE students (
    id INT PRIMARY KEY,   -- 直接写在列后
    name VARCHAR(50)
);
-- 或者作为表级约束
CREATE TABLE students (
    id INT,
    name VARCHAR(50),
    PRIMARY KEY (id)
);
-- 联合主键（两列组合唯一）
CREATE TABLE enrollments (
    student_id INT,
    course_id INT,
    enroll_date DATE,
    PRIMARY KEY (student_id, course_id)
);
-- 表已经存在时添加主键--
ALTER TABLE students ADD PRIMARY KEY (id);
```

使用场景：每个业务表都i应该有一个主键，即使是毫无意义的自增ID，经常按主键查询或使用主键进行JSON关联

### 3.2唯一索引

一个表可以有多个唯一索引，值必须唯一但可以为NULL

```sql
-- 单列唯一索引
CREATE TABLE users (
    id INT PRIMARY KEY,
    email VARCHAR(100) UNIQUE    -- 列级约束
);
-- 也可作为表级约束：UNIQUE INDEX idx_email (email)

-- 表已存在时添加
ALTER TABLE users ADD UNIQUE INDEX idx_email (email);
```

使用场景：业务上需要保证唯一的字段，如果要求不能为NULL可以添加NOT NULL的约束

### 3.3.普通索引

一个表可以有多个普通索引，允许重复和为NULL

```sql
-- 创建普通索引
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    INDEX idx_customer (customer_id),               -- 单列
    INDEX idx_customer_date (customer_id, order_date) -- 复合索引
);

-- 表已存在时添加
ALTER TABLE orders ADD INDEX idx_customer (customer_id);

-- 使用KEY关键字（等价）
CREATE TABLE orders ( ... KEY idx_customer (customer_id) );
```

使用场景：对于经常出现在WHERE、JOIN、ORDER BY、GROUP BY中的列创建普通索引
