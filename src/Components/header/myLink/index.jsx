import React, { Component } from 'react'
import { Link } from 'react-router-dom'

import './index.css'

export default class MyLink extends Component {
  render() {
    const {name} = this.props
    return (
      <Link 
      // target="_blank"
       className='header-link' {...this.props} >{name}
        <div className='button-line'></div>
      </Link>
    )
  }
}
