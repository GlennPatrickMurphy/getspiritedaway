import React, { Component } from 'react';
import { ReactiveBase, CategorySearch, ReactiveList} from '@appbaseio/reactivesearch';
import './App.css';
import planecrop from './img/planecrop.png';
import Demo from "./Demo.jsx";

class App extends Component {
    constructor(props) {
        super(props);

        this.getInnerRef = this.getInnerRef.bind(this);
        this.getLocation = this.getLocation.bind(this);
    }

    innerRef;
    getInnerRef(ref) {
        this.innerRef = ref;
    }

    getLocation() {
        this.innerRef && this.innerRef.getLocation();
    }
	render() {
		const { getInnerRef, getLocation } = this;
		return (
		    <div className="container" style={{"padding-left":"10%", "padding-right":"10%"}}>
		        {/* 
		        <article style={{ textAlign: "center" }}>
		                <Demo onError={error => console.log(error)} ref={getInnerRef} />
		                <button
		                    className="pure-button pure-button-primary"
		                    onClick={getLocation}
		                    type="button"
		                >
		                    Get location
		                </button>
	            </article>
	            */}
		        <div className="row" style={{"margin-bottom":"-30px"}}>
		          <div className="col align-self-center">
		            <h1>Get Spirited Away</h1>
		          </div>
		        </div>
		        <div className="row" style={{"padding-bottom":"20px"}}>
		          <div className="col align-self-center" >
		           <img src={planecrop} alt="plane"></img>
		          </div>
	        	</div>
				<ReactiveBase
					app="getspiritedaway_ver2"
					credentials="eJHnjdtyA:8fb5aaf5-71c4-41a1-921e-c5d88ee96777">
					<CategorySearch
						className="btrow"
						style={{"padding-left":"10%", "padding-right":"10%"}}
						componentId="searchbox"
						dataField={[
								    'description',
								    'description.autosuggest',
								    'description.keyword'
								  ]}
						placeholder="you put in your ideal vacation. we will find you the cheapest spirit flight"
					/>
					<div className="col">
					<ReactiveList
						componentId="result"
						size={10}
						dataField="City.keyword"
						pagination={true}
						
						react={{
					    	and: [
					        'searchbox'
					    	]
						}}
						onData={this.vacaresults}
					/>
					</div>
				</ReactiveBase>
			</div>
		);
	}


	vacaresults(res){
		return(
				<div className="flex book-content"> 
				<div className="flex column justify-center" style={{ marginLeft: 20 }}>
				<div className="book-header">{res.dest}</div>
				<div className="flex column justify-space-between">
					<div>{res.depart_month}{res.date}</div>
				</div>
			
				</div>	
				<div className="col price-header">${res.price}
				</div>
				</div>
			);
	}

}
export default App;