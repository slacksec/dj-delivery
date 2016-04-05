var React = require('react')
require('../css/bootstrap.min.css')

module.exports = React.createClass({
	loadRestaurantsFromServer: function() {
		$.ajax({
			url: this.props.url,
			datatype: 'json',
			cache: false, 
			success: function(data) {
				this.setState({data:data[0].name});
				console.log('setting state');
			}.bind(this)
		})
	},
	getInitialState: function() {
		return {data: []};
	},
	componentDidMount: function() {
		this.loadRestaurantsFromServer();
		setInterval(this.loadRestaurantsFromServer, this.props.pollInterval);
	},
	render: function() {
		return ( 
			<div>
			<h1>Oh shit, React works!</h1>
			<p>{this.state.data}</p>
			</div>
		)
	}
})
