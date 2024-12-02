<div id="top"/>

[![LinkedIn][linkedin-shield]][linkedin-url]
[![MIT License][license-shield]][license-url]


<br />
<div align="center">
  <a href="https://discord.com">
    <img src="https://discord.com/assets/3437c10597c1526c3dbd98c737c2bcae.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">BokBokGeh Discord Bot V2</h3>

  <p align="center">
    A personal Discord server bot for fun, upgraded from <a href="https://github.com/BernardWong97/Discord-Bot">BokBokGeh Discord Bot</a>.
    <br />
    <br />
    <a href="https://github.com/BernardWong97/Discord-Bot-V2/issues">Report Bug</a>
    ·
    <a href="https://github.com/BernardWong97/Discord-Bot-V2/issues">Request Feature</a>
  </p>
</div>


<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#features-at-a-glance">Fratures at a Glance</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#scheduled-tasks">Scheduled Tasks</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#suggestion">Suggestion</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/BernardWong97/Discord-Bot-V2)

Welcome to <b>BokBokGeh Discord Bot V2</b>, the next-generation, AI-powered version of my Discord bot!

While there are many great Discord bots available on <a href="https://top.gg">top.gg</a>, none fit my needs perfectly. So, I created this personalized bot to interact uniquely with my friends and provide humor that only we understand.

This bot is a constant work in progress, with features continuously added and refined. I enjoy exploring new capabilities introduced by <a href="https://pycord.dev/">**Pycord**</a> and improving my skills in <a href="https://www.python.org/">**Python**</a> along the way.


<p align="right">(<a href="#top">back to top</a>)</p>


## Features at a Glance

* AI-powered responses to mentions.
* Slash commands for fun and utility.
* Integration with APIs like AniList and TCGdex.
* Scheduled tasks like birthday greetings and reminders.
* Personalizable for unique server experiences.


<p align="right">(<a href="#top">back to top</a>)</p>


## Built With

* [Pycord](https://pycord.dev/)
* [Langchain](https://www.langchain.com/)
* [TCGdex](https://www.tcgdex.net/)
* [AniList](https://anilist.co/)


<p align="right">(<a href="#top">back to top</a>)</p>


## Disclaimer

This bot is designed for personal use and operates exclusively on my Discord server due to the reliance on sensitive, fixed environment variables. However, the source code is available under the <a href="https://github.com/BernardWong97/Discord-Bot-V2/blob/master/LICENSE.txt">MIT license</a>. Feel free to use and modify it as needed.


<p align="right">(<a href="#top">back to top</a>)</p>


## Usage

This bot is tailored to my server’s needs. Below are some key features and commands:

### Mention Responses

* Whenever a server member mentions the bot on a specific channel, it will use AI model to response to that mentioned individual.
  
### Slash Commands

***/send***
* Sends a message to a specified channel. (Bot owner only)
    <table>
        <tr>
            <th>Option</th>
            <th>Required</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>message</td>
            <td>Yes</td>
            <td>The message to send.</td>
        </tr>
        <tr>
            <td>channel</td>
            <td>Yes</td>
            <td>The target channel.</td>
        </tr>
    </table>

***/delete***
* Bulk deletes messages in a channel. (Bot owner only)
    <table>
        <tr>
            <th>Option</th>
            <th>Required</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>message_count</td>
            <td>Yes</td>
            <td>The number of messages to delete.</td>
        </tr>
    </table>

***/gif***
* Fetches a GIF using the [Tenor API](https://tenor.com/gifapi).
    <table>
        <tr>
            <th>Option</th>
            <th>Required</th>
            <th>Description</th>
            <th>Default</th>
        </tr>
        <tr>
            <td>keyword</td>
            <td>No</td>
            <td>The keyword to search for.</td>
            <td>chicken</td>
        </tr>
    </table>

***/manga & /anime***
* Fetch details from [AniList API](https://docs.anilist.co/) with optional filters. (e.g. format, genre, year). If no filters is provided, it will fetch 10 current seasonal details.
    <table>
        <tr>
            <th>Option</th>
            <th>Required</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>format</td>
            <td>No</td>
            <td>Filter by format.</td>
        </tr>
        <tr>
            <td>status</td>
            <td>No</td>
            <td>Filter by current release status.</td>
        </tr>
        <tr>
            <td>country</td>
            <td>No</td>
            <td>Filter by country of origin (ISO 3166-1 alpha-2).</td>
        </tr>
        <tr>
            <td>nsfw</td>
            <td>No</td>
            <td>Filter by if the media intended for 18+ adult audiences.</td>
        </tr>
        <tr>
            <td>genre</td>
            <td>No</td>
            <td>Filter by genre.</td>
        </tr>
        <tr>
            <td>source</td>
            <td>No</td>
            <td>Filter by the source.</td>
        </tr>
        <tr>
            <td>month</td>
            <td>No</td>
            <td>Filter by the release month.</td>
        </tr>
        <tr>
            <td>year</td>
            <td>No</td>
            <td>Filter by the release year.</td>
        </tr>
        <tr>
            <td>search</td>
            <td>No</td>
            <td>Filter by search query.</td>
        </tr>
    </table>

***/pokemon***
* Fetch details from [TCGdex API](https://tcgdex.dev/).
  * ***update*** - Update the cached data from API.
  * ***set*** - Set commands.
    * ***list*** - List Pokémon TCG Pocket sets.
    * ***get*** - Retrieve a Pokémon TCG Pocket set.
      <table>
          <tr>
              <th>Option</th>
              <th>Required</th>
              <th>Description</th>
          </tr>
          <tr>
              <td>set</td>
              <td>Yes</td>
              <td>The set to retrieve.</td>
          </tr>
      </table>
  * ***cards*** - Card commands.
    * ***list*** - List Pokémon TCG Pocket cards.
      <table>
          <tr>
              <th>Option</th>
              <th>Required</th>
              <th>Description</th>
          </tr>
          <tr>
              <td>set</td>
              <td>Yes</td>
              <td>Filter by set.</td>
          </tr>
      </table>
    * ***get*** - Retrieve a Pokémon TCG Pocket card.
      <table>
          <tr>
              <th>Option</th>
              <th>Required</th>
              <th>Description</th>
          </tr>
          <tr>
              <td>set</td>
              <td>Yes</td>
              <td>Filter by sets.</td>
          </tr>
          <tr>
              <td>card</td>
              <td>Yes</td>
              <td>The card to retrieve in the set.</td>
          </tr>
      </table>
    * ***id*** - Retrieve a Pokémon TCG Pocket card by ID.
      <table>
          <tr>
              <th>Option</th>
              <th>Required</th>
              <th>Description</th>
          </tr>
          <tr>
              <td>id</td>
              <td>Yes</td>
              <td>The card to retrieve by ID.</td>
          </tr>
      </table>
***/reminder***
* Manage reminders.
    * ***delete*** - Delete a reminder.
  
### Message Commands

* Right-click a message to set reminders directly via the `Apps` menu.
  * ***Remind by Duration*** - Set the reminder to trigger after a certain duration.
  * ***Remind by Time*** - Set the reminder to trigger on a specific time.


<p align="right">(<a href="#top">back to top</a>)</p>


## Scheduled Tasks

* ***Birthday Greetings*** - Wishes members happy birthday at midnight.
* ***Pokédex Updates*** - Refreshes cached Pokémon data daily from [TCGdex API](https://tcgdex.dev/).
* ***Reminder Notifications*** - Checks and sends reminders every second.


<p align="right">(<a href="#top">back to top</a>)</p>


## Roadmap

- [x] AI-powered responses
- [x] Slash commands (send, delete, GIFS, etc.)
- [x] AniList API integration
- [x] TCGdex API integration
- [x] Reminder functionality

For the full list of proposed features and known issues, see [open issues](https://github.com/BernardWong97/Discord-Bot-V2/issues).


<p align="right">(<a href="#top">back to top</a>)</p>


## Suggestion

Your feedback is invaluable! To suggest improvements or request features:
1.	Open an issue on GitHub with the `enhancement` tag.
2.	Don’t forget to give this project a star if you find it useful!


<p align="right">(<a href="#top">back to top</a>)</p>


## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<p align="right">(<a href="#top">back to top</a>)</p>


## Contact

LinkedIn: [Bernard Wong][linkedin-url]

GitHub: [BernardWong97][github-me]

Email: [ben.wc88@gmail.com](mailto:ben.wc88@gmail.com)

Project Link: [GitHub Repository][github-bot]


<p align="right">(<a href="#top">back to top</a>)</p>


[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/BernardWong97/Discord-Bot-V2/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/bernard-wong-404231152/
[product-screenshot]: attachments/profile_picture.jpeg
[github-bot]: https://github.com/BernardWong97/Discord-Bot-V2
[github-me]: https://github.com/BernardWong97