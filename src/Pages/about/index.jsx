import React, { Component } from 'react'
import { Outlet } from 'react-router-dom'
import { connect } from 'react-redux'


import './index.less'
class About extends Component {


  componentDidMount() {
    this.props.header()
  }

  render() {
    return (
      <div className='about-main common-container'>
        <Outlet></Outlet>
      </div>
    )
  }
}

export default connect(
  ()=>({}),
  {header: ()=>({type:'about'})}
  )(About)
