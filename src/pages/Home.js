import React from 'react'

class Home extends React.Component {
    construcor(props) {
    //   super(props) {
    //     // this.state={
          
    //     // }
    //   }
    }

    render() {
        return (
            <header class="App-header">
                <h1>ReviewZ</h1>
                <p>
                    Get real time feedback on how your product is doing.
                </p>
                <form>
                    <label>
                            Past your Amazon url below:
                    </label>
                    <input type="text" name="name"/>
                    <input type="submit" value="Submit"/>
                </form>
            </header>
        );
    }
  }

export default Home;