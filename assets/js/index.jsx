var React = require('react')
var App = require('./app')
var ReactDOM = require('react-dom')

ReactDOM.render(<App url='/api/restaurants/' pollInterval={10000}/>, document.getElementById('x'))
