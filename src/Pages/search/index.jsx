import React, { Component } from 'react'
import { Outlet } from 'react-router-dom'
import './index.css'

export default class Search extends Component {

  state = {
    header:{
      style:{
        backgroundImage:'url(/img/bg3_1125_500.jpg)',
        backgroundPosition:'middle',
      }
    }
  }

  render() {
    return (
      <div>
        <div className='header-bg-img' {...this.state.header}></div>
        <Outlet/>
      </div>
    )
  }
}
