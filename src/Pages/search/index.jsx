import React, { Component } from 'react'
import { Outlet } from 'react-router-dom'
import './index.css'
import { connect } from 'react-redux'


class Search extends Component {

  componentDidMount(){
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
  {header: ()=>({type:'search'})}
  )(Search)