import React, { Component } from 'react'
import './index.css'

export default class MyTab extends Component {
  render() {

    const {iClass, aLink, aText, pText } = this.props
    return (
      <div className='myTab-container'>
        <i className={iClass}></i>
        <a target='_blank' rel="noreferrer" href={aLink}>{aText}</a>
        <p>{pText}</p>
      </div>
    )
  }
}
