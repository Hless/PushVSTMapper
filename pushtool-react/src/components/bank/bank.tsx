import  * as React from 'react';
import './bank.css'
import { IParameterSettings, Parameter } from '../parameter/parameter';
import { Droppable, Draggable } from 'react-beautiful-dnd';


export interface IBankConfig {
  id:string
  name:string
  parameters:IParameterSettings[]
}

interface IProps {
  index:number
  initialBankConfig:IBankConfig
}

type IState = IBankConfig

export class Bank extends React.Component<IProps, IState> {

  public state:IState = {
    parameters: [],
    ...this.props.initialBankConfig
  }

  public render() {
    return (
      <Draggable index={this.props.index} draggableId={this.props.initialBankConfig.id}>
        {(provided) => (
          <div ref={provided.innerRef} {...provided.draggableProps} className="bank-wrapper">
            <div className="drag-handle"
              {...provided.dragHandleProps} />
          <Droppable droppableId={this.props.initialBankConfig.id} type="PERSON" direction="horizontal">
            {(innerProvided ) => (
              <div ref={innerProvided.innerRef} className="component-bank" {...innerProvided.droppableProps}>
                {this.getParameters()}
                {innerProvided.placeholder}
              </div>
             )}
          </Droppable>
          </div>

          )}
      </Draggable>
    )
  }

  private getParameters() {
    return this.props.initialBankConfig.parameters.map((param,key) => <Parameter index={key} key={param.id} initialSettings={param} />)
  }
}
