import React, { Component } from 'react'
import { Link } from 'react-router-dom'

export default class MyLink extends Component {
  render() {
    const {name} = this.props
    return (
      <Link className='header-link' {...this.props} >{name}
        <div className='button-line'></div>
      </Link>
    )
  }
}
