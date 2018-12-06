import  * as React from 'react';
import './parameter-option.scss'
import { Draggable } from 'react-beautiful-dnd';
import { InlineInput } from "../inline-input/inline-input";
import update from "immutability-helper";


export interface IParameterSettings {
  id:string
  title:string
  type:"option"|"switch"|"dial"
}

interface IProps {
  config:IParameterSettings
  index:number,
  update: (settings:IParameterSettings) => void
}


export class Parameter extends React.Component<IProps> {

  public render() {
    return (
      <Draggable draggableId={`${this.props.config.id}`} index={this.props.index}>
        {(provided) => (

          <div className="component-parameter" ref={provided.innerRef}
            {...provided.draggableProps}
            {...provided.dragHandleProps}>

            <div className="visual">
              -
            </div>
            <InlineInput defaultValue={this.props.config.title} onUpdate={this.onTitleUpdated} />

          </div>
        )}
      </Draggable>
    )
  }

  public parameterDisplay = () => {
    switch(this.props.config.type) {
      case "dial":
        return
    }
  }

  public onTitleUpdated = (value:string) => {
      this.props.update(update(this.props.config, {
        title: {
          $set: value
        }
      }))
  }
}
