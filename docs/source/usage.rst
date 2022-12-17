Usage
=====

.. _installation:


Downloading
-----------

To use TexasHoldEm, download from the
`repository <https://github.com/hpres21/texasholdem>`_:

.. code-block:: console

   $ pip install lumache

Starting a game
---------------

After that, you can play the game! To start the game, run the texasholdem.py in texasholdem/src/:

.. code-block:: console

    $ cd texasholdem/src/
    $ python texasholdem.py

Then you should see this:

.. code-block:: console

    .------..------..------..------..------.
    |T.--. ||E.--. ||X.--. ||A.--. ||S.--. |
    | :/\: || (\/) || :/\: || (\/) || :/\: |
    | (__) || :\/: || (__) || :\/: || :\/: |
    | '--'T|| '--'E|| '--'X|| '--'A|| '--'S|
    `------'`------'`------'`------'`------'

    .------..------..------..------..------..------.
    |H.--. ||O.--. ||L.--. ||D.--. ||E.--. ||M.--. |
    | :/\: || :/\: || :/\: || :/\: || (\/) || (\/) |
    | (__) || :\/: || (__) || (__) || :\/: || :\/: |
    | '--'H|| '--'O|| '--'L|| '--'D|| '--'E|| '--'M|
    `------'`------'`------'`------'`------'`------'


    Press Enter to continue...

Press Enter, and it will print out the welcome image and ask you the number of players for the game. Type a number between 2-9 and then press Enter.

.. code-block:: console

    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣀⣀⣀⣠⠔⠊⠑⠒⣷⠆⢸⢳⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⢀⠔⠋⠁⠀⠀⠉⠁⠒⠤⣄⠋⠀⠈⢧⡇⠀⠀⣰⣶⢆⠀
    ⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢉⣐⠒⠼⠿⠔⣊⣿⣿⢸⠀
    ⠀⠀⡇⠀⠀⠀⠀⢀⣤⡒⠋⣩⢉⠙⠛⢿⣿⡶⣾⣿⣿⣿⡌⠀
    ⠀⠀⠹⡄⠀⠀⢀⣾⣾⠁⢘⣭⣷⣶⠃⣿⣾⣷⣿⣿⣟⠝⠀⠀
    ⠀⠀⠀⠈⠢⣀⣸⢳⠛⡄⠀⠀⠀⠁⠀⣧⡀⢸⡽⠗⠁⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠈⠳⡄⠁⢠⠀⠀⠋⢱⢿⣷⡿⠁⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⡿⠀⢀⠐⠀⢭⣭⣽⣩⡇⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢀⣴⡇⠑⢬⣀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢀⠎⠹⡕⠠⢀⣈⠻⢿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀
    ⠀⣀⠤⠒⠒⡇⠀⠀⠈⠢⣔⣭⣙⣛⣿⣽⣇⡏⣣⣀⠀⠀⠀⠀
    ⠉⠀⠀⠀⠀⠘⡄⠀⠀⣠⠴⡟⠍⡻⠟⣿⠘⣷⣇⢧⡉⠉⠉⠁
    ⠀⠀⠀⠀⠀⠀⣇⣠⠾⠃⠀⠓⠤⢔⣄⢣⠃⡇⣿⠚⠉⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠉⢧⠁⡇⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠛⠀⠀⠀⠀⠀⠀

    Welcome to the table, partner.
    Enter the number of players:

After that, it will ask you to decide each player type.

.. code-block:: console

    Enter type for each player:
            'h'     human
            'r'     random NPC
            '1'     strategic npc 1
    p0 type:

After deciding that, you can start the bet! Simple make a legal decision in FOLD, CHECK, CALL, or input an integer value for bet or raise.

.. code-block:: condole

    p1 type: 1
    Jiachen bets $1
    p1 bets $2
    Awaiting Jiachen's decision...
            cards on table:
            pot:            $3
            current bet:    $2

            hand:           5h 10s
            stack:          $999
            already bet:    $1
    Please make a decision:

That sums up our introduction of how to play the game! Best of Luck!
