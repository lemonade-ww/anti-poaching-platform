import React, { Component } from 'react'

export default class About extends Component {
  state = {
    header:{
      style:{
        backgroundImage:'url(/img/bg6_1125_500.jpg)',
        backgroundPosition:'bottom',
      }
    }
  }
  render() {
    return (
      <div>
        <div className='header-bg-img' {...this.state.header}></div>
        关于我们介绍：。。。
      </div>
    )
  }
}
