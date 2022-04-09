import { Component, Input } from '@angular/core';
import { ChangeDetectionStrategy } from '@angular/core';
import { BoardProps, BoardState } from '@app/page/type/board';

@Component({
    selector: 'app-grid',
    templateUrl: './grid.html',
    styleUrls: ['./grid.css'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class GridComponent {
    @Input() public size: [number, number] = [9, 6];
    
    public boardProps: BoardProps = this.getBoardProps();
    public boardState: BoardState = this.getRandomBoardState();

    private getBoardProps(): BoardProps {
        return {
            rowCount: this.size[0],
            colCount: this.size[1]
        };
    }

    private getInitialBoardState(): BoardState {
        return Array(this.size[0]).fill(null).map(() =>
            Array(this.size[1]).fill(null).map(() => ({
                playerIndex: 0,
                blobCount: 0,
            }))
        );
    }

    private getRandomBoardState(): BoardState {
        return Array(this.size[0]).fill(null).map(() =>
            Array(this.size[1]).fill(null).map(() => ({
                playerIndex: Math.round(Math.random()),
                blobCount: Math.round(Math.random() * 3),
            }))
        );
    }
}
