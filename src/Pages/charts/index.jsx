import React, { Component } from 'react'



export default class Charts extends Component {
  state = {
    header:{
      style:{
        backgroundImage:'url(/img/bg5_1125_500.jpg)',
        backgroundPosition:'bottom',
      }
    }
  }
  
  render() {
    return (
      <div>
        <div className='header-bg-img' {...this.state.header}></div>
        Charts
      </div>
    )
  }
}
