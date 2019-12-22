//import { Button } from 'reactstrap';
//import React from 'react';
const Button = window.Reactstrap.Button;


const Collapse = window.Reactstrap.Collapse;
const Navbar = window.Reactstrap.Navbar;
const NavbarBrand = window.Reactstrap.NavbarBrand;
const Nav = window.Reactstrap.Nav;
const NavItem = window.Reactstrap.NavItem;
const NavLink = window.Reactstrap.NavLink;


const Router = window.ReactRouterDOM.BrowserRouter;
const Route = window.ReactRouterDOM.Route;
const ReactMarkdown = window.ReactMarkdown;

const Form = window.Reactstrap.Form;
const FormGroup = window.Reactstrap.FormGroup;
const Label = window.Reactstrap.Label;
const Input = window.Reactstrap.Input;


const UncontrolledDropdown = window.Reactstrap.UncontrolledDropdown;
const Dropdown = window.Reactstrap.Dropdown;
const DropdownToggle = window.Reactstrap.DropdownToggle;
const DropdownMenu = window.Reactstrap.DropdownMenu;
const DropdownItem = window.Reactstrap.DropdownItem;
const Spinner = window.Reactstrap.Spinner;



const axios = window.axios;

const Select = window.Select;


//import { Button } from 'reactstrap';

// Obtain the root 
const rootElement = document.getElementById('root');


class About extends React.Component {
    //

// Use the render function to return JSX component
    render() {
        return (

            <div>
                <h1>About</h1>
                <ReactMarkdown source={window.APP_CONFIG.about}/>
            </div>
        );
    }
}


// Create a ES6 class component
class MainPage extends React.Component {
    //

    constructor(props) {
        super(props);
        this.state = {
            file: null,
            unknown_loaded:false,
            known_loaded:false,
            
            imageSelected: false,
            url: null,
            isLoading: false,
            selectedOption: null,
            output:null,
            recognized:false,
            

        }
    }

    // _onFileUpload = (event) => {
    //     this.setState({
    //         rawFile: event.target.files[0],
    //         file: URL.createObjectURL(event.target.files[0]),
    //         imageSelected: true
    //     })
    // };

    // _onUrlChange = (url) => {
    //     this.state.url = url;
    //     if ((url.length > 5) && (url.indexOf("http") === 0)) {
    //         this.setState({
    //             file: url,
    //             imageSelected: true
    //         })
    //     }
    // };

    _clear = async (event) => {
        this.setState({
            file: null,
            unknown_loaded:false,
            known_loaded:false,
            unknown_loading:false,
            known_loading:false,
            
            imageSelected: false,
            url: null,
            isLoading: false,
            selectedOption: null,
            output:null,
            recognized:false,

        })
    };

    on_upload_group_pic = async (event) => {
        console.log('group_started')
        this.setState({
            unknown_loading:true,
            rawFile: event.target.files[0],
            file: URL.createObjectURL(event.target.files[0]),
            imageSelected: true 
        })
        // let resPromise = null
        const data = new FormData();
        // console.log(event.target.files[0].name);
        data.append('file', event.target.files[0]);
        let resPromise = axios.post('/api/upload_group_pic', data);
        // console.log(resPromise)
        try {
            const res = await resPromise;
            // const payload = res.data;
            // console.log(resPromise)
            this.setState({unknown_loaded:true,unknown_loading:false});
            console.log(res)
        } catch (e) {
            alert(e)
        }
    };

    on_upload_ind_pics = async (event) => {
        // this.setState({
        //     rawFile: event.target.files[0],
        //     file: URL.createObjectURL(event.target.files[0]),
        //     imageSelected: true
        // })
        console.log('ind_started')
        this.setState({known_loading:true})
        const data = new FormData();
        const files =event.target.files;

        for(var i=0;i<files.length;i++){
            data.append('file',files[i]);
        }
        
        let resPromise = axios.post('/api/upload_ind_pics',data);

        try {
            const res = await resPromise;
            // const payload = res.data;

            this.setState({known_loaded:true,known_loading: false})
            console.log(res)
        } catch (e) {
            alert(e)
        }
    };


    // _predict = async (event) => {
    //     this.setState({isLoading: true});

    //     let resPromise = null;
    //     if (this.state.rawFile) {
    //         const data = new FormData();
    //         data.append('file', this.state.rawFile);
    //         resPromise = axios.post('/api/classify', data);
    //     } else {
    //         resPromise = axios.get('/api/classify', {
    //             params: {
    //                 url: this.state.file
    //             }
    //         });
    //     }

    //     try {
    //         const res = await resPromise;
    //         const payload = res.data;

    //         this.setState({predictions: payload.predictions, isLoading: false});
    //         console.log(payload)
    //     } catch (e) {
    //         alert(e)
    //     }
    // };

    recognize=async()=>{
        let resPromise= axios.get('/api/recognize');
        try {
           
            const response=await resPromise;
            // const file=response.data;
            // this.state.output=file;
            // console.log(this.state.output)
            // console.log(this.state.recognized);
            this.setState({recognized:true})
            console.log('Recognition done:',this.state.recognized);
            // console.log('success');
        }catch (e) {
            alert(e)
        }
    };


    // renderPrediction() {

    //     return (
    //         <ul>
    //             {this.state.output}
    //         </ul>
    //     )

    //     } else {
    //         return null
    //     }
    // }

    handleChange = (selectedOption) => {
        this.setState({selectedOption});
        console.log(`Option selected:`, selectedOption);
    };

    // sampleUrlSelected  = (item) => {
    //     this._onUrlChange(item.url);
    // };
    render() {
        const sampleImages = APP_CONFIG.sampleImages;
        return (
            <div>
                <h3>{APP_CONFIG.description}</h3>

                {/* <p>Upload Images</p> */}

                <Form>
                    {/* <FormGroup>
                        <div>
                            <p>Provide a Url</p>
                            <div>

                                <UncontrolledDropdown >
                                    <DropdownToggle caret>
                                        Sample Image Url
                                    </DropdownToggle>
                                    <DropdownMenu>
                                        {sampleImages.map(si =>
                                            <DropdownItem onClick={()=>this.sampleUrlSelected(si)}>
                                                {si.name}
                                            </DropdownItem>)
                                        }

                                    </DropdownMenu>
                                </UncontrolledDropdown>

                            </div>
                            <Input value={this.state.url} name="file" onChange={(e)=>this._onUrlChange(e.target.value)}
                            />
                        </div>
                    </FormGroup> */}

                    {/* <h3>OR</h3> */}
                    <FormGroup id={"upload_button"}>
                        <div>
                            <p><strong>Upload Individual Pictures</strong></p>
                        </div>
                        <Label for="imageUpload">
                                <input type="file" name="files" id="imageUpload" accept=".png, .jpg, .jpeg" ref='files'
                                        onChange={this.on_upload_ind_pics} multiple/>
                                <span className="btn btn-primary">Upload</span>                               
                        </Label>
                    </FormGroup>

                    {this.state.known_loading && (
                        <div>
                            <Spinner color="primary" type="grow" style={{width: '5rem', height: '5rem'}}/>

                        </div>
                    )}

                    {/* <FormGroup id={"upload_button"}>
                        <div>
                            <p><strong>Upload Individual Pictures</strong></p>
                        </div>
                        <Label for="imageUpload">
                            <form action='/api/upload_ind_pics' method="POST" enctype="multipart/form-data">
                                <input type="file" name="files" id="imageUpload" accept=".png, .jpg, .jpeg" 
                                         multiple/>
                                <span className="btn btn-primary">Upload</span>
                                <div> </div>
                                <input type="submit" value="Submit" id="upload-button"/>
                                
                            </form> 
                        </Label>
                    </FormGroup> */}

                    <FormGroup id={"upload_button"}>
                        <div>
                            <p><strong>Upload Group Picture</strong></p>
                        </div>
                        <Label for="imageUpload1">
                            <Input type="file" name="file" id="imageUpload1" accept=".png, .jpg, .jpeg" ref="file"
                                   onChange={this.on_upload_group_pic}/>
                            
                            <span className="btn btn-primary">Upload</span>
                        </Label>
                    </FormGroup>
                    
                    {this.state.unknown_loading && (
                        <div>
                            <Spinner color="primary" type="grow" style={{width: '5rem', height: '5rem'}}/>

                        </div>
                    )}

                    <img src={this.state.file} className={"img-preview"} hidden={!this.state.imageSelected}/>

                    <FormGroup>
                        <Button color="success" onClick={this.recognize}
                                disabled={!(this.state.unknown_loaded && this.state.known_loaded)}>
                                     Recognize</Button>
                        <span className="p-1 "/>
                        <Button color="danger" onClick={this._clear}> Clear</Button>
                    </FormGroup>


                    {/* {this.state.isLoading && (
                        <div>
                            <Spinner color="primary" type="grow" style={{width: '5rem', height: '5rem'}}/>

                        </div>
                    )} */}

                </Form>
                
                
                <img src={"./static/output.jpg?t=" + new Date().getTime()} className={"img-preview"} hidden={!this.state.recognized} />
                


            </div>
        );
    }
}



class CustomNavBar extends React.Component {


    render() {
        const link = APP_CONFIG.code;
        return (
            <Navbar color="light" light fixed expand="md">
                <NavbarBrand href="/">{APP_CONFIG.title}</NavbarBrand>
                {/* <Collapse navbar>
                    <Nav className="ml-auto" navbar>
                        <NavItem>
                            <NavLink href="/about">About</NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href={link}>GitHub</NavLink>
                        </NavItem>

                    </Nav>
                </Collapse> */}
            </Navbar>
        )
    }
}

// Create a function to wrap up your component
function App() {
    return (


        <Router>
            <div className="App">
                <CustomNavBar/>
                <div>
                    <main role="main" className="container">
                        <Route exact path="/" component={MainPage}/>
                        <Route exact path="/about" component={About}/>

                    </main>


                </div>
            </div>
        </Router>
    )
}

(async () => {
    const response = await fetch('/config');
    const body = await response.json();

    window.APP_CONFIG = body;

    // Use the ReactDOM.render to show your component on the browser
    ReactDOM.render(
        <App/>,
        rootElement
    )
})();


