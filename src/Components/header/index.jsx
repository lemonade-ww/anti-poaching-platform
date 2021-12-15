import React, { Component } from 'react'
import {Link} from 'react-router-dom'

export default class Header extends Component {
  render() {
    return (
      <div>
        <Link to='/home'>HOME</Link>
        <Link to='/charts'>CHARTS</Link>
        <Link to='/search'>SEARCH</Link>
      </div>
    )
  }
}
