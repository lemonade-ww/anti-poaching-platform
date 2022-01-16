import React, { Component } from 'react'
import './index.css'

export default class MyTab extends Component {
  render() {

    const {iClass, aLink, aText, pText } = this.props
    return (
      <div className='myTab-container'>
        <i class={iClass}></i>
        <a href={aLink}>{aText}</a>
        <p>{pText}</p>
      </div>
    )
  }
}
