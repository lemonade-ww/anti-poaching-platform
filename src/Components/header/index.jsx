import React, { Component } from 'react'
import MyLink from './myLink'
import {notification} from 'antd';
import './index.css'
import {connect} from 'react-redux'

class Header extends Component {

  state = {
    isExpand: false, // 初始状态：未展开
    isclicking: false
  }

  openNotificationWithIcon = type => {
    notification[type]({
      message: '提示 Notification',
      description:
        '后台数据完善中，检索功能暂时无法使用，敬请期待！',
    });
  };

  expandSearch = () => {
    const { isExpand, isclicking } = this.state
    if (!isclicking) {
      if (!isExpand) { // 如果是折叠状态，则下拉时会触发获取焦点事件
        // 开启isClicking，防止在获取焦点前改变状态
        this.setState({ isclicking: true })
        setTimeout(() => {
          this.input.focus() // 获取焦点
          // 关闭isClicking，此时可以改变状态
          this.setState({ isclicking: false })
        }, 400)
      }
      this.setState({ isExpand: !isExpand })
    }
  }

  onNavClick = ()=>{
    this.setState({ isExpand: false })
  }

  render() {
    const { isExpand } = this.state
    return (
      <div className={isExpand ? 'header-main header-main-expand' : 'header-main'}>

        <div className='header-bg-img' {...this.props.style}></div>
       
        <div className='header-front-interface'>
          <div className='header-main-container'>
            <a href="http://localhost:3000/" className='header-logo'>
              <img className='logo-img' src="/img/盾牌,安全,保护.png" alt="logo" />
              <p>中国野生动物盗猎大数据平台</p>
              <p>antipoach.cn</p>
            </a>

            <div className='header-menu'>
              <div className='header-login'>
                <a href="#">联系我们</a>
                <a href="#">注册</a>
                <a href="#">登陆</a>
              </div>

              <nav className='header-nav'>
                <MyLink onClick={this.onNavClick} className='header-link' to='/' name='主页' />
                <MyLink onClick={this.onNavClick} className='header-link' to='/charts' name='图表' />
                <MyLink onClick={this.onNavClick} className='header-link' to='/search' name='高级检索' />
                <MyLink onClick={this.onNavClick} className='header-link' to='/about' name='关于' />
              </nav>
            </div>
          </div>

          <form className='header-main-container header-expand-area'>
            <input 
            onFocus={()=>this.openNotificationWithIcon('info')}
            className='header-input' type="text" placeholder='输入物种名、地区等进行快速搜索' ref={c => this.input = c} />
            <button className='header-submit' type="submit"></button>

            <svg className={isExpand ? "search-icon search-icon-expand" : "search-icon"}
              ref={c => this.search = c} onClick={this.expandSearch} viewBox="0 0 1024 1024">
              <path d="M453.818182 23.272727C704.465455 23.272727 907.636364 226.443636 907.636364 477.090909c0 35.746909-4.142545 70.981818-12.264728 105.192727a46.545455 46.545455 0 0 1-90.577454-21.504c6.469818-27.182545 9.751273-55.202909 9.751273-83.688727C814.545455 277.876364 653.032727 116.363636 453.818182 116.363636 254.603636 116.363636 93.090909 277.876364 93.090909 477.090909 93.090909 676.305455 254.603636 837.818182 453.818182 837.818182c101.003636 0 195.211636-41.658182 262.981818-113.826909a46.545455 46.545455 0 0 1 63.650909-3.979637c2.978909 1.792 5.818182 3.956364 8.401455 6.446546l213.201454 205.684363a45.707636 45.707636 0 0 1 0.581818 65.233455l-0.581818 0.581818a46.545455 46.545455 0 0 1-65.233454 0.581818l-185.390546-178.827636A452.305455 452.305455 0 0 1 453.818182 930.909091C203.170909 930.909091 0 727.738182 0 477.090909S203.170909 23.272727 453.818182 23.272727z m76.613818 179.828364c86.714182 23.598545 147.2 76.078545 177.245091 154.973091a46.545455 46.545455 0 0 1-86.993455 33.140363c-19.176727-50.362182-55.994182-82.315636-114.688-98.280727a46.545455 46.545455 0 1 1 24.436364-89.832727z" fill="#ffffff">
              </path></svg>
            <span className={isExpand ? 'header-closebtn header-closebtn-expand' : 'header-closebtn'} onClick={this.expandSearch} >×</span>
          </form>

        </div>
      </div>

    )
  }
}


const mapStateToProps = state => ({style:state}) // 映射状态

export default connect(mapStateToProps)(Header)