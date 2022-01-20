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

1. React组件内的方法，需要用**箭头函数**，否则this会丢失，无法获取`this.state`
2. svg标签，更改颜色需要操纵内部的path标签的fill属性，无法用color直接改变颜色
3. transition属性有`transition-property`和`transition-duration`
4. input框如果想要手动获取焦点，使用`element.focus()`操作DOM，但是一旦获取焦点，相关的trasition就会被打断，因此可以给transition一个定时器


### 2022年1月9日

主要内容

1. 修改扩展搜索框的定位
2. 添加Home页面的主要结构
3. 试图用 Ant Design V4 来添加搜索框、轮播图，发现引入Antd的css文件会污染原本的样式，而且轮播图的图片一直显示不出来，考虑到网站前台没有太多需要UI 组件的地方，且Antd修改风格太麻烦，遂放弃。明天试试看Bootstrap的轮播图好了。晚安(￣o￣) . z Z


### 2022年1月12日

主要内容:

重新用flex布局写了Header组件：
   
 - 外容器宽度100%
 - 主体宽度 max 1056px  min 1000px  (参考知乎)
 - 主体布局为flex，`space-between`


### 2022年1月14日

主要内容：

完成首页（Home组件）的轮播图、搜索框区域的整体：

  - 使用了Boostrap V5.1.3 的组件及图标，用CDN引入
  - 引入Boostrap的CSS之后，会对全局产生影响，主要的问题在p标签和Link组件超链接
      - p标签会增加`margin-bottom`
      - Link组件（不确定是否a标签都会受影响）在`hover`状态下的文字会变成蓝色
  - 针对上面两个问题，进行了单独的样式处理
  - 研究了Boostrap的输入框组件的属性：
      - 比如，focus状态下的阴影： `border-shadow`

感受：

调整CSS样式真的好慢，研究boostrap的既定样式需要花时间。不过最终做出来的成品特别有成就感！加油！！！！！！！

### 2022年1月15日

主要内容

1. 微调按钮样式
2. 构思主页下半部分
3. 了解AntV L7的应用，根据文档，需要调用高德地图API，申请开发者key
4. 免费注册了高德地图开发账号，发现网站提供自定义地图接口，可以在线制作地图，很方便
  
接下来的安排：
1. 简单设计 1 首页 并完成 2 内容页 和 3 文章页 （不难）
2. 研究一下高德地图制作 数据类型支持情况
3. 后端接口的问题。 emmmmmm  头疼。

### 2022年1月16日

主要内容

1. 统一修改内容区宽度，解决小于最小宽度时，右侧一些组件出现空白的问题
   **最大宽度：1056px 最小宽度 960px**
2. 主题色：#f26649   主题字体色：#C44D34
3. 完成首页的Tab栏及内容区域，新定义小组件 `MyTab`

### 2022年1月17日

主要内容

1. 完成首页的文章栏，用到卡片组件
2. 注意：每个部分的外部容器要设置max-width和min-width来保证出现滚动条的时候，右侧不会出现空白，不能用width：100%（窗口的100%）来设置。
```css
   max-width: 1056px;
  min-width: 960px;
  margin: 0 auto;
```

接下来：
1. 内容页 和 文章页 
2. 研究一下高德地图制作 数据类型支持情况
3. 后端接口的问题。


### 2022年1月18日

主要内容：

完成footer组件

### 2022年1月19日

主要内容：

1. 为导航栏的其他页面添加底图
2. 学习React Router的二级路由（Nested routes），可以通过':xxxid'传递参数，但只能在函数式组件中使用`useparams`来接
3. 回顾函数式组件的`useState` hook
4. 试图做case详情页：
   - 用了一条数据放在state内，模拟返回的数据
   - 初步构思页面结构：左侧为“相关搜索”，根据case内容形成的高级搜索的简化版，用Accordion（手风琴演奏；风琴褶）组件。
   - 右侧为case内容展示区，用表格组件

太晚了，昨天又熬夜了，哎今天不困，但是又熬夜。昼夜颠倒。好烦

***发现bug：导航栏的底图需要和Header组件的快速搜索框联动，需要用到Redux！！！***



### 2022年1月20日

主要内容：

1. 完成详情页
2. 修复错误：1. class =》 className   2. key={v4()}  使用uuid为遍历的子元素添加key 
3. 学习/复习到的内容：

    - useState、useEffect 在函数式组件中的使用
    - lable标签的 for 属性，是为了和input联动。 在React里这个属性叫 htmlFor