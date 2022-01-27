import React, { Component } from 'react'
import { connect } from 'react-redux'




class Charts extends Component {
  
  componentDidMount() {
    this.props.header()
  }

  render() {
    return (
      <div>
        Charts
      </div>
    )
  }
}

export default connect(
  ()=>({}),
  {header: ()=>({type:'charts'})}
  )(Charts)
