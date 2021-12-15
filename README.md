页面构建记录


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
    <Route path="/home" render={() => <Navigate to="/home" />} />
  </Routes>
  ```