import { Component, Input, ViewChildren } from '@angular/core';
import { QueryList, ElementRef } from '@angular/core';
import { AfterViewInit } from '@angular/core';
import { ChangeDetectionStrategy } from '@angular/core';
import { BoardProps, BoardCellState } from '@app/page/type/board';

@Component({
    selector: 'app-cell',
    templateUrl: './cell.html',
    styleUrls: ['./cell.css'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class CellComponent implements AfterViewInit {
    @Input() public pos!: [number, number];
    @Input() public props!: BoardProps;
    @Input() public state!: BoardCellState;

    @ViewChildren('blob', { read: ElementRef })
    public blobElements!: QueryList<ElementRef<HTMLElement>>;

    private calculateBlobColor(playerIndex: number): string {
        switch (playerIndex) {
            case 0: return '#ff6600';
            case 1: return '#00dd63';
            default: throw new Error('player index out of range');
        }
    }

    private updateBlobColors(): void {
        const blobColor = this.calculateBlobColor(this.state.playerIndex);
        this.blobElements.forEach((elem) =>
            elem.nativeElement.style.setProperty('--blob-color', blobColor)
        );
    }

    public ngAfterViewInit(): void {    
        this.updateBlobColors()
    }
}
