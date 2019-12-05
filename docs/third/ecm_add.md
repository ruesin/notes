---
title: ecmall数据库操作方法add，判断是否插入成功。
date: 2014-07-08 17:22:26
categories: 三方产品
tags: 
- ecmall
- 商派产品
---

使用ecmall的add时，可能会碰到这种情况，调用model类的add方法插入数据时，如果插入的数据的主键不是自增ID，就会返回空值，无法判断是否插入成功。  
刚开始时没注意，还以为是因为我的sql语句写错了呢，后来翻了下base.model类下的add方法，才发现是本身的BUG，不得不再说一遍，ecmall代码写的实在是太…..

```
function add($data, $compatible = false){
    if (empty($data) || !$this->dataEnough($data))    {
        return false;
    }
    $data = $this->_valid($data);
    if (!$data){
        $this->_error('no_valid_data');
        return false;
    }
    $insert_info = $this->_getInsertInfo($data);
    $mode = $compatible ? 'REPLACE' : 'INSERT';
    $this->db->query("{$mode} INTO {$this->table}{$insert_info['fields']} VALUES{$insert_info['values']}");
    $insert_id = $this->db->insert_id();
    if ($insert_id){
        if ($insert_info['length'] > 1){
            for ($i = $insert_id; $i 
```

这里用的是php内置函数mysql\_insert\_id()返回了上一步 INSERT 操作产生的 ID。如果上一查询没有产生 AUTO\_INCREMENT 的 ID，则 mysql\_insert\_id() 返回 0。  
而我们很多时候会需要用到判断插入是否成功，所以我把原方法改了下，先判断是否有插入ID，如果没有，就判断是否执行成功，成功就返回true。

```
function add($data, $compatible = false){
    if (empty($data) || !$this->dataEnough($data)){
        return false;
    }
    $data = $this->_valid($data);
    if (!$data){
        $this->_error('no_valid_data');
        return false;
    }
    $insert_info = $this->_getInsertInfo($data);
    $mode = $compatible ? 'REPLACE' : 'INSERT';

    $query=$this->db->query("{$mode} INTO {$this->table}{$insert_info['fields']} VALUES{$insert_info['values']}");
    
    $insert_id = $this->db->insert_id();
    
    if ($insert_id){
        if ($insert_info['length'] > 1){
            for ($i = $insert_id; $i 
```

以上仅仅是为了满足本项目中开发而更改的，算是为各位看官起一个抛砖引玉的作用吧。
