"""
Visualization Module
Creates charts and plots for portfolio analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Dict
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Visualizer:
    """Create visualizations for portfolio backtest results"""

    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize Visualizer

        Args:
            style: Matplotlib style
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

        sns.set_palette("husl")
        self.colors = sns.color_palette("husl", 10)

    def plot_portfolio_value(
        self,
        results: pd.DataFrame,
        benchmark: bool = True,
        figsize: tuple = (14, 6)
    ):
        """
        Plot portfolio value over time

        Args:
            results: Backtest results DataFrame
            benchmark: Include benchmark if available
            figsize: Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)

        # Plot portfolio value
        ax.plot(
            results.index,
            results['portfolio_value'],
            label='Portfolio',
            linewidth=2,
            color=self.colors[0]
        )

        # Plot benchmark if available
        if benchmark and 'benchmark_value' in results.columns:
            ax.plot(
                results.index,
                results['benchmark_value'],
                label='Benchmark',
                linewidth=2,
                color=self.colors[1],
                linestyle='--'
            )

        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Portfolio Value ($)', fontsize=12)
        ax.set_title('Portfolio Value Over Time', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_returns(
        self,
        results: pd.DataFrame,
        benchmark: bool = True,
        figsize: tuple = (14, 10)
    ):
        """
        Plot cumulative and daily returns

        Args:
            results: Backtest results DataFrame
            benchmark: Include benchmark if available
            figsize: Figure size
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)

        # Cumulative returns
        ax1.plot(
            results.index,
            results['cumulative_returns'] * 100,
            label='Portfolio',
            linewidth=2,
            color=self.colors[0]
        )

        if benchmark and 'benchmark_cumulative' in results.columns:
            ax1.plot(
                results.index,
                results['benchmark_cumulative'] * 100,
                label='Benchmark',
                linewidth=2,
                color=self.colors[1],
                linestyle='--'
            )

        ax1.set_ylabel('Cumulative Returns (%)', fontsize=12)
        ax1.set_title('Cumulative Returns', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        # Daily returns
        ax2.bar(
            results.index,
            results['returns'] * 100,
            label='Daily Returns',
            color=self.colors[2],
            alpha=0.6
        )

        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Daily Returns (%)', fontsize=12)
        ax2.set_title('Daily Returns', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        plt.tight_layout()
        return fig

    def plot_drawdown(
        self,
        results: pd.DataFrame,
        figsize: tuple = (14, 6)
    ):
        """
        Plot drawdown over time

        Args:
            results: Backtest results DataFrame
            figsize: Figure size
        """
        # Calculate drawdown
        cumulative = (1 + results['returns']).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max

        fig, ax = plt.subplots(figsize=figsize)

        ax.fill_between(
            results.index,
            drawdown * 100,
            0,
            color=self.colors[3],
            alpha=0.5,
            label='Drawdown'
        )

        ax.plot(
            results.index,
            drawdown * 100,
            color=self.colors[3],
            linewidth=1
        )

        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Drawdown (%)', fontsize=12)
        ax.set_title('Portfolio Drawdown', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)

        plt.tight_layout()
        return fig

    def plot_allocation(
        self,
        allocations: pd.DataFrame,
        figsize: tuple = (14, 6)
    ):
        """
        Plot allocation weights over time

        Args:
            allocations: DataFrame of allocation weights
            figsize: Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)

        # Stack plot
        ax.stackplot(
            allocations.index,
            *[allocations[col] * 100 for col in allocations.columns],
            labels=allocations.columns,
            colors=self.colors[:len(allocations.columns)],
            alpha=0.8
        )

        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Allocation (%)', fontsize=12)
        ax.set_title('Portfolio Allocation Over Time', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_rolling_metrics(
        self,
        results: pd.DataFrame,
        window: int = 252,
        figsize: tuple = (14, 10)
    ):
        """
        Plot rolling performance metrics

        Args:
            results: Backtest results DataFrame
            window: Rolling window size
            figsize: Figure size
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)

        returns = results['returns']

        # Rolling return
        rolling_return = returns.rolling(window).apply(
            lambda x: (1 + x).prod() ** (252/len(x)) - 1
        )
        ax1.plot(results.index, rolling_return * 100, color=self.colors[0], linewidth=1.5)
        ax1.set_title(f'Rolling {window}-Day Annualized Return', fontweight='bold')
        ax1.set_ylabel('Return (%)', fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        # Rolling volatility
        rolling_vol = returns.rolling(window).std() * np.sqrt(252)
        ax2.plot(results.index, rolling_vol * 100, color=self.colors[1], linewidth=1.5)
        ax2.set_title(f'Rolling {window}-Day Volatility', fontweight='bold')
        ax2.set_ylabel('Volatility (%)', fontsize=11)
        ax2.grid(True, alpha=0.3)

        # Rolling Sharpe
        rolling_sharpe = returns.rolling(window).apply(
            lambda x: np.sqrt(252) * x.mean() / x.std() if x.std() != 0 else 0
        )
        ax3.plot(results.index, rolling_sharpe, color=self.colors[2], linewidth=1.5)
        ax3.set_title(f'Rolling {window}-Day Sharpe Ratio', fontweight='bold')
        ax3.set_ylabel('Sharpe Ratio', fontsize=11)
        ax3.set_xlabel('Date', fontsize=11)
        ax3.grid(True, alpha=0.3)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        # Rolling max drawdown
        cumulative = (1 + returns).cumprod()
        rolling_max = cumulative.rolling(window, min_periods=1).max()
        rolling_dd = (cumulative - rolling_max) / rolling_max
        ax4.fill_between(results.index, rolling_dd * 100, 0, color=self.colors[3], alpha=0.5)
        ax4.plot(results.index, rolling_dd * 100, color=self.colors[3], linewidth=1)
        ax4.set_title(f'Rolling {window}-Day Max Drawdown', fontweight='bold')
        ax4.set_ylabel('Drawdown (%)', fontsize=11)
        ax4.set_xlabel('Date', fontsize=11)
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_returns_distribution(
        self,
        results: pd.DataFrame,
        figsize: tuple = (14, 6)
    ):
        """
        Plot returns distribution

        Args:
            results: Backtest results DataFrame
            figsize: Figure size
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        returns = results['returns'].dropna() * 100

        # Histogram
        ax1.hist(returns, bins=50, color=self.colors[0], alpha=0.7, edgecolor='black')
        ax1.axvline(returns.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {returns.mean():.2f}%')
        ax1.axvline(returns.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {returns.median():.2f}%')
        ax1.set_xlabel('Returns (%)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title('Returns Distribution', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # Q-Q plot
        from scipy import stats
        stats.probplot(returns, dist="norm", plot=ax2)
        ax2.set_title('Q-Q Plot (Normal Distribution)', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_correlation_matrix(
        self,
        returns_data: pd.DataFrame,
        figsize: tuple = (10, 8)
    ):
        """
        Plot correlation matrix heatmap

        Args:
            returns_data: DataFrame of returns for multiple assets
            figsize: Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)

        correlation = returns_data.corr()

        sns.heatmap(
            correlation,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )

        ax.set_title('Asset Correlation Matrix', fontsize=14, fontweight='bold')

        plt.tight_layout()
        return fig

    def create_interactive_dashboard(
        self,
        results: pd.DataFrame,
        allocations: Optional[pd.DataFrame] = None
    ):
        """
        Create interactive dashboard using Plotly

        Args:
            results: Backtest results DataFrame
            allocations: Allocation weights DataFrame

        Returns:
            Plotly figure
        """
        # Create subplots
        n_rows = 3 if allocations is not None else 2
        fig = make_subplots(
            rows=n_rows,
            cols=2,
            subplot_titles=(
                'Portfolio Value',
                'Cumulative Returns',
                'Drawdown',
                'Daily Returns',
                'Allocation' if allocations is not None else '',
                'Rolling Sharpe' if allocations is not None else ''
            ),
            specs=[
                [{"secondary_y": False}, {"secondary_y": False}],
                [{"secondary_y": False}, {"secondary_y": False}],
                [{"secondary_y": False}, {"secondary_y": False}] if allocations is not None else None
            ][:(n_rows)]
        )

        # Portfolio value
        fig.add_trace(
            go.Scatter(x=results.index, y=results['portfolio_value'], name='Portfolio', line=dict(width=2)),
            row=1, col=1
        )
        if 'benchmark_value' in results.columns:
            fig.add_trace(
                go.Scatter(x=results.index, y=results['benchmark_value'], name='Benchmark',
                          line=dict(width=2, dash='dash')),
                row=1, col=1
            )

        # Cumulative returns
        fig.add_trace(
            go.Scatter(x=results.index, y=results['cumulative_returns']*100, name='Cumulative Returns',
                      line=dict(width=2)),
            row=1, col=2
        )

        # Drawdown
        cumulative = (1 + results['returns']).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max * 100

        fig.add_trace(
            go.Scatter(x=results.index, y=drawdown, fill='tozeroy', name='Drawdown',
                      line=dict(width=1)),
            row=2, col=1
        )

        # Daily returns
        fig.add_trace(
            go.Bar(x=results.index, y=results['returns']*100, name='Daily Returns'),
            row=2, col=2
        )

        # Allocation (if provided)
        if allocations is not None:
            for col in allocations.columns:
                fig.add_trace(
                    go.Scatter(x=allocations.index, y=allocations[col]*100, name=col,
                              stackgroup='one'),
                    row=3, col=1
                )

            # Rolling Sharpe
            rolling_sharpe = results['returns'].rolling(252).apply(
                lambda x: np.sqrt(252) * x.mean() / x.std() if x.std() != 0 else 0
            )
            fig.add_trace(
                go.Scatter(x=results.index, y=rolling_sharpe, name='Rolling Sharpe',
                          line=dict(width=2)),
                row=3, col=2
            )

        # Update layout
        fig.update_layout(
            height=300 * n_rows,
            showlegend=True,
            title_text="Portfolio Backtest Dashboard",
            title_font_size=20
        )

        return fig

    @staticmethod
    def save_figure(fig, filename: str, dpi: int = 300):
        """
        Save figure to file

        Args:
            fig: Matplotlib or Plotly figure
            filename: Output filename
            dpi: DPI for matplotlib figures
        """
        if isinstance(fig, plt.Figure):
            fig.savefig(filename, dpi=dpi, bbox_inches='tight')
            print(f"Figure saved to {filename}")
        else:
            fig.write_html(filename)
            print(f"Interactive figure saved to {filename}")
