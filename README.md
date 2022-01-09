# 页面构建记录


### 2021年12月14日

主要内容：

1. 确定首页主要外观
  基本模仿对象：https://www.ala.org.au/
2. 创建react项目

### 2021年12月15日

主要内容：

1. 创建项目目录，学习目录结构
2. 用react-router-dom 创建路由，react-router从11月起从V5升级到了V6，学习了新用法：
  - 取消 `Switch`，改用 `Routes`
  - 取消 `component={组件名}`，改用 `element={<组件名/>}`
  - 取消 `Redirect to`，改用`Navigate to` ： 
   ```js
   <Routes>
    <Route path='/home' element={<Home/>}></Route>
   </Routes>
   ```

### 2022年1月7日

主要内容

1. react-router v6的重定向问题：
   ```js
   <Route path="*" element={<Navigate to="/" />} />
   ```

2. 自定义link组件
3. 添加Header组件文本

### 2022年1月8日

主要内容

1. 写Header组件样式

注意点：

1. React组件内的方法，需要用箭头函数，否则this会丢失，无法获取this.state
2. svg标签，更改颜色需要操纵内部的path标签的fill属性，无法用color直接改变颜色
3. transition属性有transition-property和transition-duration
4. input框如果想要手动获取焦点，使用element.focus()操作DOM，但是一旦获取焦点，相关的trasition就会被打断，因此可以给transition一个定时器


### 2022年1月9日

主要内容

1. 修改扩展搜索框的定位
2. 添加Home页面的主要结构
3. 试图用 Ant Design V4 来添加搜索框、轮播图，发现引入Antd的css文件会污染原本的样式，而且轮播图的图片一直显示不出来，考虑到网站前台没有太多需要UI 组件的地方，且Antd修改风格太麻烦，遂放弃。明天试试看Bootstrap的轮播图好了。晚安(￣o￣) . z Z