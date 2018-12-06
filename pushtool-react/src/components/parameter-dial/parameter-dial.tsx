import  * as React from 'react';
import './parameter-dial.scss'
import * as svg from './dial.svg';


interface Props {
  value:string
}
export class ParameterDial extends React.Component<Props> {

  public render() {
    return (
      <div className="parameter-dial">
        <h4>{this.props.value}</h4>
        
        <div className="dial-graphic">
          <div className="dial">
            <img src={svg} />
          </div>
          <div className="dial overlay">
              <img src={svg} />
          </div>
        </div>

      </div>
    )
  }
}
