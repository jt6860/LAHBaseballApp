import { Component } from '@angular/core';
import { BatterStatsComponent } from "../batter-stats/batter-stats.component";
import { PitcherStatsComponent } from "../pitcher-stats/pitcher-stats.component";
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  imports: [BatterStatsComponent, PitcherStatsComponent, CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  showBattingStats = true; 
  showPitchingStats = false; 

  pitchingChange() {
    this.showPitchingStats = true;
    this.showBattingStats = false;
  }

  battingChange() {
    this.showPitchingStats = false;
    this.showBattingStats = true;
  }
}
