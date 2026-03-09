"""
stock-data CLI -- direct tool invocation without MCP overhead.

Usage:
    stock-data <tool_name> [key=value ...]
    stock-data stock_prices symbol=600519 market=sh limit=60
    stock-data okx_prices instId=BTC-USDT bar=1D limit=30
    stock-data --list
"""
import sys
import inspect
import argparse


def _build_tool_registry() -> dict:
    """Build name->function map from open_stock_data exports.

    Imports are deferred to here to avoid heavy initialization at module load time.
    """
    from open_stock_data.tools import ALL_TOOLS
    return ALL_TOOLS


def _resolve_defaults(fn, kwargs: dict) -> dict:
    """Fill in defaults from Pydantic Field objects for missing args.

    Tool functions use Field("sh", description="...") as parameter defaults.
    When called directly (not through FastMCP), the default is a FieldInfo object,
    not the actual value. This function extracts the real default.
    """
    from pydantic.fields import FieldInfo

    sig = inspect.signature(fn)
    for name, param in sig.parameters.items():
        if name not in kwargs and isinstance(param.default, FieldInfo):
            if param.default.default is not inspect.Parameter.empty:
                kwargs[name] = param.default.default
    return kwargs


def _coerce_args(fn, raw_kwargs: dict) -> dict:
    """Coerce CLI string args to the types expected by the function.

    Uses the function's type annotations to determine the correct type.
    Falls back to str if no annotation is found.
    """
    from pydantic.fields import FieldInfo

    sig = inspect.signature(fn)
    coerced = {}
    for key, value in raw_kwargs.items():
        param = sig.parameters.get(key)
        if param is not None:
            # Get the target type from annotation
            ann = param.annotation
            if ann is inspect.Parameter.empty:
                # Try to infer from Field default
                if isinstance(param.default, FieldInfo):
                    default_val = param.default.default
                    if default_val is not inspect.Parameter.empty and default_val is not None:
                        ann = type(default_val)
            # Coerce to the target type
            if ann is int:
                coerced[key] = int(value)
            elif ann is float:
                coerced[key] = float(value)
            elif ann is bool:
                coerced[key] = value.lower() in ("true", "1", "yes")
            else:
                # str or unknown → keep as string
                coerced[key] = value
        else:
            # Unknown parameter — pass as-is (let the function handle the error)
            coerced[key] = value
    return coerced


def main():
    parser = argparse.ArgumentParser(
        prog="stock-data",
        description="Stock data CLI - direct tool invocation without MCP overhead",
        epilog="Example: stock-data stock_prices symbol=600519 market=sh limit=60",
    )
    parser.add_argument("tool", nargs="?", help="Tool name (e.g. stock_prices)")
    parser.add_argument("args", nargs="*", help="Arguments as key=value pairs")
    parser.add_argument("--list", action="store_true", help="List all available tools")

    args = parser.parse_args()

    # Load .env before anything else
    from .env import load_env
    load_env()

    # Build tool registry (lazy import of open_stock_data)
    registry = _build_tool_registry()

    if args.list or not args.tool:
        for name in sorted(registry.keys()):
            print(name)
        return

    tool_name = args.tool
    if tool_name not in registry:
        print(f"Unknown tool: {tool_name}", file=sys.stderr)
        print(f"Use 'stock-data --list' to see available tools", file=sys.stderr)
        sys.exit(1)

    # Parse key=value args
    raw_kwargs = {}
    for arg in args.args:
        if "=" in arg:
            k, v = arg.split("=", 1)
            raw_kwargs[k] = v
        else:
            print(f"Invalid argument format: {arg} (expected key=value)", file=sys.stderr)
            sys.exit(1)

    fn = registry[tool_name]
    kwargs = _coerce_args(fn, raw_kwargs)
    kwargs = _resolve_defaults(fn, kwargs)

    try:
        result = fn(**kwargs)
        if result is not None:
            print(result)
    except TypeError as e:
        print(f"Argument error: {e}", file=sys.stderr)
        # Show expected parameters
        sig = inspect.signature(fn)
        params = []
        for name, param in sig.parameters.items():
            from pydantic.fields import FieldInfo
            if isinstance(param.default, FieldInfo):
                desc = param.default.description or ""
                default = param.default.default
                if default is inspect.Parameter.empty:
                    params.append(f"  {name} (required): {desc}")
                else:
                    params.append(f"  {name}={default}: {desc}")
            elif param.default is not inspect.Parameter.empty:
                params.append(f"  {name}={param.default}")
            else:
                params.append(f"  {name} (required)")
        print(f"\nUsage: stock-data {tool_name} " + " ".join(
            f"{p.split(':')[0].strip()}=<value>" for p in params
        ), file=sys.stderr)
        print(f"\nParameters:", file=sys.stderr)
        for p in params:
            print(p, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
