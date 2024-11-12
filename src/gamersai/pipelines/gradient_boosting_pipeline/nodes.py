import logging
import pandas as pd
import wandb
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
import wandb.sklearn

def train_gradient_boosting_model(X_train: pd.DataFrame, y_train: pd.Series, X_test: pd.DataFrame, y_test: pd.Series, parameters: dict) -> GradientBoostingRegressor:
    """Trains a Gradient Boosting Regressor model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for the target.

    Returns:
        Trained Gradient Boosting model.
    """
    #model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=101)
    model = GradientBoostingRegressor(n_estimators=parameters["n_estimators_boosting"], learning_rate=parameters["learning_rate_boosting"], max_depth=parameters["max_depth_boosting"], random_state=parameters["random_state_boosting"])
    model.fit(X_train, y_train)
    
    #wandb.sklearn.plot_regressor(model=model, X_train=X_train, X_test=X_test,y_train=y_train,y_test=y_test)
    
    return model

def evaluate_gradient_boosting_model(
    regressor: GradientBoostingRegressor, X_train:pd.DataFrame,y_train:pd.Series, X_test: pd.DataFrame, y_test: pd.Series
):
    """Calculates and logs the coefficient of determination for the Gradient Boosting model.

    Args:
        regressor: Trained Gradient Boosting model.
        X_test: Testing data of independent features.
        y_test: Testing data for the target.
    """
    run = wandb.init(
        # set the wandb project where this run will be logged
        project="gamersAI",
        name = "GB",
        # track hyperparameters and run metadata
        config=regressor.get_params()
    )
    wandb.sklearn.plot_learning_curve(model=regressor, X=X_train,y=y_train)
    wandb.sklearn.plot_summary_metrics(regressor, X_train, y_train, X_test, y_test)
    run = wandb.run
    y_pred = regressor.predict(X_test)
    score = r2_score(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("GB model has a coefficient R^2 of %.3f on test data.", score)
    to_log = {
            "score":score
              }
    run.log(to_log)
    run.finish()