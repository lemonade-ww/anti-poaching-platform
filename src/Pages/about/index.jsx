import React, { Component } from 'react'
import { connect } from 'react-redux'



class About extends Component {


  componentDidMount() {
    this.props.header()
  }

  render() {
    return (
      <div>
        关于我们介绍：。。。
      </div>
    )
  }
}

export default connect(
  ()=>({}),
  {header: ()=>({type:'about'})}
  )(About)
