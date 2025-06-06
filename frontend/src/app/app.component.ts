import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { CurrencyService } from './currency.service';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatButtonModule,
    MatSelectModule,
    MatTableModule,
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  private fb = inject(FormBuilder);
  private currencyService = inject(CurrencyService);

  dateRangeForm: FormGroup = this.fb.group({
  range: this.fb.group({
    start: [null],
    end: [null]
  })
});

  currencies: any[] = [];
  filteredCurrencies: any[] = [];

  displayedColumns = ['code', 'name', 'mid', 'date'];

  years: number[] = [];
  quarters = ['Q1', 'Q2', 'Q3', 'Q4'];
  months = Array.from({ length: 12 }, (_, i) => ({
    value: i + 1,
    label: new Date(0, i).toLocaleString('default', { month: 'long' }),
  }));
  days = Array.from({ length: 31 }, (_, i) => i + 1);

  selectedYear: number | null = null;
  selectedQuarter: string | null = null;
  selectedMonth: number | null = null;
  selectedDay: number | null = null;

  fetchCurrenciesRange(): void {
  const rangeGroup = this.dateRangeForm.get('range') as FormGroup;
  const startDate: Date = rangeGroup.value.start;
  const endDate: Date = rangeGroup.value.end;

  if (!startDate || !endDate) return;

  const requests = [];
  const current = new Date(startDate);

  while (current <= endDate) {
    const formatted = current.toISOString().split('T')[0];
    requests.push(this.currencyService.getCurrenciesByDate(formatted));
    current.setDate(current.getDate() + 1);
  }

  Promise.all(requests.map(r => r.toPromise()))
    .then(results => {
      const merged = results.flat().sort((a, b) => a.code.localeCompare(b.code));
      this.currencies = merged;
      this.filteredCurrencies = [...merged];
      this.extractAvailableYears();
    })
    .catch(err => {
      console.error('Błąd pobierania danych:', err);
      this.currencies = [];
      this.filteredCurrencies = [];
    });
}
  extractAvailableYears(): void {
    const yearsSet = new Set<number>();
    for (const c of this.currencies) {
      const year = new Date(c.date).getFullYear();
      yearsSet.add(year);
    }
    this.years = Array.from(yearsSet).sort((a, b) => b - a);
  }

  applyFilters(): void {
    this.filteredCurrencies = this.currencies.filter((currency) => {
      const d = new Date(currency.date);
      return (
        (!this.selectedYear || d.getFullYear() === this.selectedYear) &&
        (!this.selectedQuarter || this.getQuarter(d) === this.selectedQuarter) &&
        (!this.selectedMonth || d.getMonth() + 1 === this.selectedMonth) &&
        (!this.selectedDay || d.getDate() === this.selectedDay)
      );
    });
  }

  resetFilters(): void {
    this.selectedYear = null;
    this.selectedQuarter = null;
    this.selectedMonth = null;
    this.selectedDay = null;
    this.filteredCurrencies = [...this.currencies];
  }

  getQuarter(d: Date): string {
    const m = d.getMonth() + 1;
    if (m <= 3) return 'Q1';
    if (m <= 6) return 'Q2';
    if (m <= 9) return 'Q3';
    return 'Q4';
  }
}
