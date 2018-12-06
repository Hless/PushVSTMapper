import  * as React from 'react';
import './bank.scss'
import { IParameterSettings, Parameter } from '../parameter/parameter';
import { Droppable, Draggable } from 'react-beautiful-dnd';
import { InlineInput } from "../inline-input/inline-input";

export interface IBankConfig {
  id:string
  name:string
  parameters:IParameterSettings[]
}

export interface BankUpdateEvent {
  id:string
  changes:{
    name?:string
    parameter?:IParameterSettings
  }
}

interface IProps {
  index:number
  config: IBankConfig
  update:(event:BankUpdateEvent) => void
}

interface State {
  editingCancelled:boolean
}

export class Bank extends React.Component<IProps> {

  public state:State = {
    editingCancelled: true
  }

  private inputRef:React.RefObject<HTMLInputElement> = React.createRef();

  public render() {
    return (
      <Draggable index={this.props.index} draggableId={this.props.config.id}>
        {(provided) => (
          <div ref={provided.innerRef} {...provided.draggableProps} className="bank-wrapper">
            <div className="drag-handle"
              {...provided.dragHandleProps}>
              <i className="far fa-arrows-alt" />
            </div>
          <Droppable droppableId={this.props.config.id} type="PERSON" direction="horizontal">
            {(innerProvided ) => (
              <div ref={innerProvided.innerRef} className="component-bank" {...innerProvided.droppableProps}>
                {this.getParameters()}
                {innerProvided.placeholder}
              </div>
             )}
          </Droppable>
            <div className="bank-name">
              <InlineInput defaultValue={this.props.config.name}
                onUpdate={this.onNameUpdate} />
            </div>
          </div>

          )}
      </Draggable>
    )
  }

  private onNameUpdate = (value:string) => {
    this.props.update({
      id: this.props.config.id,
      changes: {
        name: value
      }
    })
  }

  private onParameterUpdate = (value:IParameterSettings) => {
    this.props.update({
      id: this.props.config.id,
      changes: {
        parameter: value
      }
    })
  }

  private getParameters() {
    return this.props.config.parameters.map((param,key) => <Parameter
      index={key}
      key={param.id}
      config={param}
      editable={true}
      update={this.onParameterUpdate} />)
  }
}
