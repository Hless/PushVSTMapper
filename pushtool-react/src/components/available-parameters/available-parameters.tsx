import  * as React from 'react';
import './available-parameters.scss'
import { IParameterSettings, Parameter } from '../parameter/parameter';
import { Droppable } from 'react-beautiful-dnd';

interface IProps {

  parameters:IParameterSettings[]
}



export class AvailableParameters extends React.Component<IProps> {

  public render() {
    return (
      <Droppable droppableId="available-parameters" type="available">
        {(innerProvided ) => (
          <div ref={innerProvided.innerRef} className="available-parameters" {...innerProvided.droppableProps}>
            {this.getParameters()}
            {innerProvided.placeholder}
          </div>
         )}
      </Droppable>
    )
  }



  private onParameterUpdate = (value:IParameterSettings) => {
    return value;
  }

  private getParameters() {

    console.log(this.props.parameters)
    return this.props.parameters.map((param,key) => <Parameter
      index={key}
      key={param.id}
      config={param}
      editable={false}
      update={this.onParameterUpdate} />)
  }
}
