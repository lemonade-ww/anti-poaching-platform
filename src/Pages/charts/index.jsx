import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Outlet } from 'react-router-dom'




class Charts extends Component {
  
  componentDidMount() {
    this.props.header()
  }

  render() {
    return (
      <div>
        <Outlet/>
      </div>
    )
  }
}

export default connect(
  ()=>({}),
  {header: ()=>({type:'charts'})}
  )(Charts)
