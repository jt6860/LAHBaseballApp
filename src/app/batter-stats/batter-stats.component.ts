import { Component, OnInit } from '@angular/core';
import { BatterStats, DataService, PitcherStats } from '../data.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-batter-stats',
  standalone: true,
  templateUrl: './batter-stats.component.html',
  styleUrls: ['./batter-stats.component.css'],
  imports: [FormsModule, CommonModule],
  providers: [DataService]
})
export class BatterStatsComponent implements OnInit {
  batterStats: BatterStats[] = [];
  selectedSeason: number = 2023;
  sortedBatters: any[] = [];
  sortBy: string = 'name';
  sortDirection: 'asc' | 'desc' = 'asc'; 
  years: number[] = [];

  constructor(private dataService: DataService) { 
    this.years = this.generateYearsArray(1871, 2023);
  }

  ngOnInit() {
    this.loadBatterStats();
  }

  loadBatterStats() {
    this.dataService.getBatterStats(this.selectedSeason).subscribe({
      next: (data) => { 
        this.batterStats = data; 
        this.sortedBatters = [...this.batterStats];
      },
      error: (error) => {
        console.error('Error fetching batter stats:', error); 
      }
    });
  }

  sortData() {
    this.sortedBatters.sort((a, b) => {
      if (a[this.sortBy] < b[this.sortBy]) {
        return this.sortDirection === 'asc' ? -1 : 1;
      }
      if (a[this.sortBy] > b[this.sortBy]) {
        return this.sortDirection === 'asc' ? 1 : -1;
      }
      return 0;
    });
  }

  sort(column: string) {
    this.sortBy = column;
    this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    this.sortData();
  }

  isStatExceptional(stat: number, threshold: number) {
    return stat >= threshold;
  }

  generateYearsArray(startYear: number, endYear: number): number[] {
    const yearArray: number[] = [];
    for (let year = startYear; year <= endYear; year++) {
      yearArray.push(year);
    }
    return yearArray;
  }
}