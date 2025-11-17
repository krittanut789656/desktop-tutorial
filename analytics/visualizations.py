"""
Data Visualization Module for ETF Portfolio Analytics

This module provides comprehensive visualization functions for the 3 main analytics insights:
1. Risk-Adjusted Performance Analysis
2. Optimal Rebalancing Frequency Analysis
3. DCA vs Lump Sum Market Timing Analysis

Features:
- Professional matplotlib/seaborn styling
- Publication-ready charts
- Customizable colors and themes
- Export to PNG and PDF formats

Dependencies: matplotlib, seaborn, pandas, numpy

Author: ETF Portfolio Backtesting System
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set professional styling
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 10


# =============================================================================
# INSIGHT 1: Risk-Adjusted Performance Visualization
# =============================================================================

def plot_risk_return_scatter(
    portfolio_data: List[Dict],
    benchmark_data: Optional[Dict] = None,
    output_file: str = 'risk_return_scatter.png',
    dpi: int = 300
) -> None:
    """
    Create Risk-Return Scatter Plot comparing multiple portfolios

    Args:
        portfolio_data: List of dicts with keys: 'name', 'return', 'volatility', 'sharpe'
        benchmark_data: Optional dict for benchmark (SPY) with same keys
        output_file: Output filename (PNG or PDF)
        dpi: Resolution for PNG output

    Example:
        portfolio_data = [
            {'name': 'Portfolio 1', 'return': 12.5, 'volatility': 15.2, 'sharpe': 0.82},
            {'name': 'Portfolio 2', 'return': 10.1, 'volatility': 12.3, 'sharpe': 0.82}
        ]
        benchmark_data = {'name': 'SPY', 'return': 11.2, 'volatility': 14.1, 'sharpe': 0.79}
    """
    try:
        fig, ax = plt.subplots(figsize=(12, 8))

        # Extract data
        names = [p['name'] for p in portfolio_data]
        returns = [p['return'] for p in portfolio_data]
        volatilities = [p['volatility'] for p in portfolio_data]
        sharpes = [p['sharpe'] for p in portfolio_data]

        # Color map based on Sharpe ratio
        colors = plt.cm.RdYlGn([(s - min(sharpes)) / (max(sharpes) - min(sharpes) + 0.01)
                                 for s in sharpes])

        # Plot portfolios
        scatter = ax.scatter(volatilities, returns, s=200, c=colors,
                           alpha=0.6, edgecolors='black', linewidth=1.5)

        # Add portfolio labels
        for i, name in enumerate(names):
            ax.annotate(name, (volatilities[i], returns[i]),
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=9, fontweight='bold')

        # Plot benchmark if provided
        if benchmark_data:
            ax.scatter([benchmark_data['volatility']], [benchmark_data['return']],
                      s=300, c='red', marker='D', alpha=0.8,
                      edgecolors='black', linewidth=2, label=benchmark_data['name'])
            ax.annotate(benchmark_data['name'],
                       (benchmark_data['volatility'], benchmark_data['return']),
                       xytext=(5, -15), textcoords='offset points',
                       fontsize=10, fontweight='bold', color='red')

        # Add efficient frontier guide line (45-degree)
        ax.plot([0, max(volatilities) * 1.1], [0, max(returns) * 1.1],
               'k--', alpha=0.3, linewidth=1, label='1:1 Risk-Return')

        ax.set_xlabel('Volatility (Annualized Standard Deviation %)', fontweight='bold')
        ax.set_ylabel('Return (Annualized %)', fontweight='bold')
        ax.set_title('Risk-Return Analysis: Portfolio Comparison',
                    fontweight='bold', fontsize=14, pad=20)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
        logger.info(f"Risk-Return scatter plot saved to {output_file}")
        plt.close()

    except Exception as e:
        logger.error(f"Error creating risk-return scatter plot: {e}")
        raise


def plot_drawdown_comparison(
    portfolio_dd_data: Dict[str, List[Tuple[datetime, float]]],
    benchmark_dd_data: Optional[List[Tuple[datetime, float]]] = None,
    output_file: str = 'drawdown_comparison.png',
    dpi: int = 300
) -> None:
    """
    Create Drawdown Chart comparing portfolios with benchmark

    Args:
        portfolio_dd_data: Dict of portfolio_name -> [(date, drawdown_pct), ...]
        benchmark_dd_data: Optional list of [(date, drawdown_pct), ...] for SPY
        output_file: Output filename
        dpi: Resolution

    Example:
        portfolio_dd_data = {
            'Portfolio 1': [(datetime(2020,1,1), 0), (datetime(2020,3,1), -15.2), ...],
            'Portfolio 2': [(datetime(2020,1,1), 0), (datetime(2020,3,1), -12.1), ...]
        }
    """
    try:
        fig, ax = plt.subplots(figsize=(14, 7))

        # Plot each portfolio
        colors = plt.cm.tab10(range(len(portfolio_dd_data)))
        for i, (name, data) in enumerate(portfolio_dd_data.items()):
            dates = [d[0] for d in data]
            drawdowns = [d[1] for d in data]
            ax.plot(dates, drawdowns, label=name, linewidth=2,
                   color=colors[i], alpha=0.8)

            # Highlight maximum drawdown
            min_dd = min(drawdowns)
            min_idx = drawdowns.index(min_dd)
            ax.scatter([dates[min_idx]], [min_dd], s=100,
                      color=colors[i], marker='v', zorder=5,
                      edgecolors='black', linewidth=1.5)
            ax.annotate(f'{min_dd:.1f}%', (dates[min_idx], min_dd),
                       xytext=(10, -10), textcoords='offset points',
                       fontsize=8, fontweight='bold')

        # Plot benchmark if provided
        if benchmark_dd_data:
            dates = [d[0] for d in benchmark_dd_data]
            drawdowns = [d[1] for d in benchmark_dd_data]
            ax.plot(dates, drawdowns, label='SPY (Benchmark)',
                   linewidth=2.5, color='red', linestyle='--', alpha=0.9)

            min_dd = min(drawdowns)
            min_idx = drawdowns.index(min_dd)
            ax.scatter([dates[min_idx]], [min_dd], s=120,
                      color='red', marker='v', zorder=5,
                      edgecolors='black', linewidth=2)
            ax.annotate(f'SPY: {min_dd:.1f}%', (dates[min_idx], min_dd),
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=9, fontweight='bold', color='red')

        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Drawdown (%)', fontweight='bold')
        ax.set_title('Maximum Drawdown Analysis: Recovery Patterns',
                    fontweight='bold', fontsize=14, pad=20)
        ax.legend(loc='lower left')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

        # Format y-axis as percentage
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))

        plt.tight_layout()
        plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
        logger.info(f"Drawdown comparison chart saved to {output_file}")
        plt.close()

    except Exception as e:
        logger.error(f"Error creating drawdown comparison chart: {e}")
        raise


# =============================================================================
# INSIGHT 2: Optimal Rebalancing Frequency Visualization
# =============================================================================

def plot_rebalancing_frequency_comparison(
    strategy_data: List[Dict],
    output_file: str = 'rebalancing_frequency_comparison.png',
    dpi: int = 300
) -> None:
    """
    Create bar chart comparing returns across different rebalancing frequencies

    Args:
        strategy_data: List of dicts with keys: 'strategy', 'return', 'volatility',
                      'sharpe', 'total_costs'
        output_file: Output filename
        dpi: Resolution

    Example:
        strategy_data = [
            {'strategy': 'Buy & Hold', 'return': 10.5, 'volatility': 15.2,
             'sharpe': 0.69, 'total_costs': 0},
            {'strategy': 'Monthly', 'return': 11.2, 'volatility': 14.8,
             'sharpe': 0.76, 'total_costs': 1250}
        ]
    """
    try:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        strategies = [d['strategy'] for d in strategy_data]
        returns = [d['return'] for d in strategy_data]
        sharpes = [d['sharpe'] for d in strategy_data]
        costs = [d['total_costs'] for d in strategy_data]

        # Chart 1: Returns and Sharpe Ratio
        x = np.arange(len(strategies))
        width = 0.35

        bars1 = ax1.bar(x - width/2, returns, width, label='Annualized Return (%)',
                       color='steelblue', alpha=0.8, edgecolor='black', linewidth=1.2)

        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%', ha='center', va='bottom', fontweight='bold')

        ax1_twin = ax1.twinx()
        bars2 = ax1_twin.bar(x + width/2, sharpes, width, label='Sharpe Ratio',
                            color='orange', alpha=0.8, edgecolor='black', linewidth=1.2)

        for bar in bars2:
            height = bar.get_height()
            ax1_twin.text(bar.get_x() + bar.get_width()/2., height,
                         f'{height:.3f}', ha='center', va='bottom', fontweight='bold')

        ax1.set_xlabel('Rebalancing Strategy', fontweight='bold')
        ax1.set_ylabel('Annualized Return (%)', fontweight='bold', color='steelblue')
        ax1_twin.set_ylabel('Sharpe Ratio', fontweight='bold', color='orange')
        ax1.set_title('Performance Comparison Across Rebalancing Frequencies',
                     fontweight='bold', fontsize=14, pad=20)
        ax1.set_xticks(x)
        ax1.set_xticklabels(strategies, rotation=15, ha='right')
        ax1.tick_params(axis='y', labelcolor='steelblue')
        ax1_twin.tick_params(axis='y', labelcolor='orange')
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.legend(loc='upper left')
        ax1_twin.legend(loc='upper right')

        # Chart 2: Cost-Benefit Analysis
        net_returns = [r - (c/10000) for r, c in zip(returns, costs)]  # Adjust scale

        bars3 = ax2.bar(strategies, costs, color='crimson', alpha=0.7,
                       edgecolor='black', linewidth=1.2, label='Total Transaction Costs')

        for i, (bar, cost) in enumerate(zip(bars3, costs)):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'${cost:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

        ax2.set_xlabel('Rebalancing Strategy', fontweight='bold')
        ax2.set_ylabel('Transaction Costs ($)', fontweight='bold', color='crimson')
        ax2.set_title('Transaction Cost Analysis by Rebalancing Frequency',
                     fontweight='bold', fontsize=14, pad=20)
        ax2.tick_params(axis='y', labelcolor='crimson')
        ax2.set_xticklabels(strategies, rotation=15, ha='right')
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.legend(loc='upper left')

        plt.tight_layout()
        plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
        logger.info(f"Rebalancing frequency comparison saved to {output_file}")
        plt.close()

    except Exception as e:
        logger.error(f"Error creating rebalancing frequency chart: {e}")
        raise


def plot_portfolio_value_over_time(
    strategy_data: Dict[str, List[Tuple[datetime, float]]],
    output_file: str = 'portfolio_value_over_time.png',
    dpi: int = 300
) -> None:
    """
    Create line chart showing portfolio value evolution for different strategies

    Args:
        strategy_data: Dict of strategy_name -> [(date, portfolio_value), ...]
        output_file: Output filename
        dpi: Resolution

    Example:
        strategy_data = {
            'Buy & Hold': [(datetime(2020,1,1), 100000), (datetime(2020,2,1), 102500), ...],
            'Monthly Rebalancing': [(datetime(2020,1,1), 100000), ...]
        }
    """
    try:
        fig, ax = plt.subplots(figsize=(14, 8))

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        linestyles = ['-', '--', '-.', ':', '-']

        final_values = {}
        for i, (strategy, data) in enumerate(strategy_data.items()):
            dates = [d[0] for d in data]
            values = [d[1] for d in data]

            ax.plot(dates, values, label=strategy, linewidth=2.5,
                   color=colors[i % len(colors)],
                   linestyle=linestyles[i % len(linestyles)],
                   alpha=0.85)

            final_values[strategy] = values[-1]

        # Add final value annotations
        for strategy, final_val in final_values.items():
            last_date = list(strategy_data[strategy])[-1][0]
            ax.annotate(f'${final_val:,.0f}', (last_date, final_val),
                       xytext=(10, 0), textcoords='offset points',
                       fontsize=9, fontweight='bold')

        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Portfolio Value ($)', fontweight='bold')
        ax.set_title('Portfolio Value Evolution: Rebalancing Strategy Comparison',
                    fontweight='bold', fontsize=14, pad=20)
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)

        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'${y:,.0f}'))

        plt.tight_layout()
        plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
        logger.info(f"Portfolio value over time chart saved to {output_file}")
        plt.close()

    except Exception as e:
        logger.error(f"Error creating portfolio value chart: {e}")
        raise


# =============================================================================
# INSIGHT 3: DCA vs Lump Sum Visualization
# =============================================================================

def plot_dca_vs_lumpsum_comparison(
    lumpsum_data: List[Tuple[datetime, float]],
    dca_data: List[Tuple[datetime, float]],
    entry_points: List[datetime],
    output_file: str = 'dca_vs_lumpsum_comparison.png',
    dpi: int = 300
) -> None:
    """
    Create comparison chart for DCA vs Lump Sum strategies

    Args:
        lumpsum_data: [(date, portfolio_value), ...] for Lump Sum
        dca_data: [(date, portfolio_value), ...] for DCA
        entry_points: List of dates when DCA investments occurred
        output_file: Output filename
        dpi: Resolution
    """
    try:
        fig, ax = plt.subplots(figsize=(14, 8))

        # Extract data
        ls_dates = [d[0] for d in lumpsum_data]
        ls_values = [d[1] for d in lumpsum_data]
        dca_dates = [d[0] for d in dca_data]
        dca_values = [d[1] for d in dca_data]

        # Plot strategies
        ax.plot(ls_dates, ls_values, label='Lump Sum (Invest 100% on Day 1)',
               linewidth=3, color='#d62728', alpha=0.8)
        ax.plot(dca_dates, dca_values, label='Dollar Cost Averaging (DCA)',
               linewidth=3, color='#2ca02c', alpha=0.8)

        # Mark DCA entry points
        for entry_date in entry_points[:10]:  # Show first 10 to avoid clutter
            idx = next((i for i, d in enumerate(dca_dates) if d >= entry_date), None)
            if idx:
                ax.scatter([dca_dates[idx]], [dca_values[idx]], s=80,
                          color='green', marker='o', alpha=0.6, zorder=5)

        # Add annotation for entry points
        if len(entry_points) > 0:
            ax.annotate('DCA Entry Points', xy=(entry_points[0], dca_values[0]),
                       xytext=(50, 30), textcoords='offset points',
                       fontsize=9, color='green', fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='green', lw=1.5))

        # Calculate and show final difference
        final_ls = ls_values[-1]
        final_dca = dca_values[-1]
        diff_pct = ((final_ls - final_dca) / final_dca) * 100

        winner = "Lump Sum" if final_ls > final_dca else "DCA"
        color = '#d62728' if final_ls > final_dca else '#2ca02c'

        ax.text(0.02, 0.98,
               f'Final Values:\nLump Sum: ${final_ls:,.0f}\nDCA: ${final_dca:,.0f}\n' +
               f'Winner: {winner} (+{abs(diff_pct):.2f}%)',
               transform=ax.transAxes, fontsize=11, fontweight='bold',
               verticalalignment='top', bbox=dict(boxstyle='round',
               facecolor=color, alpha=0.2, edgecolor=color, linewidth=2))

        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Portfolio Value ($)', fontweight='bold')
        ax.set_title('DCA vs Lump Sum Investment Strategy Comparison',
                    fontweight='bold', fontsize=14, pad=20)
        ax.legend(loc='lower right', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'${y:,.0f}'))

        plt.tight_layout()
        plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
        logger.info(f"DCA vs Lump Sum comparison chart saved to {output_file}")
        plt.close()

    except Exception as e:
        logger.error(f"Error creating DCA vs Lump Sum comparison chart: {e}")
        raise


def plot_win_rate_by_market_condition(
    market_conditions: Dict[str, Dict],
    output_file: str = 'win_rate_by_market_condition.png',
    dpi: int = 300
) -> None:
    """
    Create bar chart showing DCA win rate across different market conditions

    Args:
        market_conditions: Dict with keys 'bull', 'bear', 'neutral'
                          Each contains: {'dca_wins': int, 'total_days': int,
                                        'win_rate': float, 'avg_outperformance': float}
        output_file: Output filename
        dpi: Resolution

    Example:
        market_conditions = {
            'bull': {'dca_wins': 120, 'total_days': 500, 'win_rate': 24.0,
                    'avg_outperformance': -2.5},
            'bear': {'dca_wins': 380, 'total_days': 400, 'win_rate': 95.0,
                    'avg_outperformance': 8.3}
        }
    """
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        conditions = list(market_conditions.keys())
        win_rates = [market_conditions[c]['win_rate'] for c in conditions]
        avg_outperformance = [market_conditions[c].get('avg_outperformance', 0)
                             for c in conditions]

        colors = {'bull': '#2ca02c', 'bear': '#d62728', 'neutral': '#ff7f0e'}
        bar_colors = [colors.get(c, 'steelblue') for c in conditions]

        # Chart 1: Win Rate
        bars1 = ax1.bar(conditions, win_rates, color=bar_colors, alpha=0.8,
                       edgecolor='black', linewidth=1.5)

        for bar, wr in zip(bars1, win_rates):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{wr:.1f}%', ha='center', va='bottom',
                    fontweight='bold', fontsize=12)

        ax1.set_ylabel('DCA Win Rate (%)', fontweight='bold')
        ax1.set_title('DCA Win Rate by Market Condition',
                     fontweight='bold', fontsize=13, pad=15)
        ax1.set_ylim(0, max(win_rates) * 1.15)
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.axhline(y=50, color='black', linestyle='--', linewidth=1, alpha=0.5)

        # Chart 2: Average Outperformance
        bars2 = ax2.bar(conditions, avg_outperformance, color=bar_colors, alpha=0.8,
                       edgecolor='black', linewidth=1.5)

        for bar, outperf in zip(bars2, avg_outperformance):
            height = bar.get_height()
            va = 'bottom' if height >= 0 else 'top'
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{outperf:+.2f}%', ha='center', va=va,
                    fontweight='bold', fontsize=12)

        ax2.set_ylabel('Average Outperformance (%)', fontweight='bold')
        ax2.set_title('DCA Average Outperformance by Market Condition',
                     fontweight='bold', fontsize=13, pad=15)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=1.5)

        plt.tight_layout()
        plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
        logger.info(f"Win rate by market condition chart saved to {output_file}")
        plt.close()

    except Exception as e:
        logger.error(f"Error creating win rate by market condition chart: {e}")
        raise


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_summary_dashboard(
    risk_return_file: str,
    drawdown_file: str,
    rebalancing_file: str,
    dca_comparison_file: str,
    output_file: str = 'analytics_dashboard.png',
    dpi: int = 200
) -> None:
    """
    Create a comprehensive 2x2 dashboard combining all key visualizations

    Args:
        risk_return_file: Path to risk-return scatter plot
        drawdown_file: Path to drawdown comparison
        rebalancing_file: Path to rebalancing frequency chart
        dca_comparison_file: Path to DCA vs Lump Sum chart
        output_file: Output filename for dashboard
        dpi: Resolution
    """
    try:
        from matplotlib import image as mpimg

        fig, axes = plt.subplots(2, 2, figsize=(20, 16))

        images = [risk_return_file, drawdown_file, rebalancing_file, dca_comparison_file]
        titles = ['Risk-Return Analysis', 'Drawdown Analysis',
                 'Rebalancing Strategy', 'DCA vs Lump Sum']

        for ax, img_file, title in zip(axes.flat, images, titles):
            try:
                img = mpimg.imread(img_file)
                ax.imshow(img)
                ax.axis('off')
                ax.set_title(title, fontweight='bold', fontsize=14, pad=10)
            except FileNotFoundError:
                ax.text(0.5, 0.5, f'Image not found:\n{img_file}',
                       ha='center', va='center', fontsize=12)
                ax.axis('off')

        plt.suptitle('ETF Portfolio Analytics Dashboard',
                    fontweight='bold', fontsize=18, y=0.995)
        plt.tight_layout()
        plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
        logger.info(f"Analytics dashboard saved to {output_file}")
        plt.close()

    except Exception as e:
        logger.error(f"Error creating summary dashboard: {e}")
        raise


def save_chart_multiple_formats(
    fig,
    base_filename: str,
    formats: List[str] = ['png', 'pdf'],
    dpi: int = 300
) -> None:
    """
    Save matplotlib figure in multiple formats

    Args:
        fig: Matplotlib figure object
        base_filename: Base filename without extension
        formats: List of formats (png, pdf, svg)
        dpi: Resolution for raster formats
    """
    try:
        for fmt in formats:
            output_file = f"{base_filename}.{fmt}"
            fig.savefig(output_file, dpi=dpi if fmt == 'png' else None,
                       bbox_inches='tight', format=fmt)
            logger.info(f"Chart saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving chart in multiple formats: {e}")
        raise


if __name__ == "__main__":
    print("Data Visualization Module for ETF Portfolio Analytics")
    print("=" * 60)
    print("\nAvailable visualization functions:")
    print("\nInsight 1 - Risk-Adjusted Performance:")
    print("  - plot_risk_return_scatter()")
    print("  - plot_drawdown_comparison()")
    print("\nInsight 2 - Optimal Rebalancing:")
    print("  - plot_rebalancing_frequency_comparison()")
    print("  - plot_portfolio_value_over_time()")
    print("\nInsight 3 - DCA vs Lump Sum:")
    print("  - plot_dca_vs_lumpsum_comparison()")
    print("  - plot_win_rate_by_market_condition()")
    print("\nUtility Functions:")
    print("  - create_summary_dashboard()")
    print("  - save_chart_multiple_formats()")
    print("\nImport this module to use visualization functions in your analytics scripts.")
