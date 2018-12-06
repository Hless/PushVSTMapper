import  * as React from 'react';
import './inline-input.scss'


interface Props {
  defaultValue:string
  onUpdate:(value:string) => void
}

interface State {
  editingCancelled:boolean
}

export class InlineInput extends React.Component<Props, State> {

  public state:State = {
    editingCancelled: true
  }

  private inputRef:React.RefObject<HTMLInputElement> = React.createRef();

  public render() {
    return (
      <input className="inline-input" defaultValue={this.props.defaultValue}
        ref={this.inputRef}
        onKeyUp={this.editNameKeyUp}
        onFocus={this.onFocus}
        onBlur={this.onBlur} />
)
  }

  private onFocus = (_:React.FocusEvent) => {
    this.setState({ editingCancelled: false });
  }

  private onBlur = (_:React.FocusEvent) => {
    if(this.state.editingCancelled) {
      this.inputRef.current!.value = this.props.defaultValue;
      return;
    }
    this.props.onUpdate(this.inputRef.current!.value)
  }

  private editNameKeyUp = (event:React.KeyboardEvent<HTMLInputElement>) => {
    if(event.keyCode !== 27 && event.keyCode !== 13)
      return;

    this.setState({
      editingCancelled: event.keyCode === 27
    },
    () => {
      this.inputRef.current!.blur();
    });
  }
}
